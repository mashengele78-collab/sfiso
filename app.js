(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const els = {
    imageInput: $("#imageInput"),
    imageDrop: $("#imageDrop"),
    imageEmpty: $("#imageEmpty"),
    imageLoaded: $("#imageLoaded"),
    imageThumb: $("#imageThumb"),
    imageName: $("#imageName"),
    imageMeta: $("#imageMeta"),
    imageError: $("#imageError"),
    removeImage: $("#removeImage"),
    characterSection: $("#characterSection"),
    scriptInput: $("#scriptInput"),
    scriptDrop: $("#scriptDrop"),
    scriptFile: $("#scriptFile"),
    scriptType: $("#scriptType"),
    scriptName: $("#scriptName"),
    scriptMeta: $("#scriptMeta"),
    scriptError: $("#scriptError"),
    removeScript: $("#removeScript"),
    scriptText: $("#scriptText"),
    scriptSection: $("#scriptSection"),
    wordCount: $("#wordCount"),
    stepCount: $("#stepCount"),
    durationEstimate: $("#durationEstimate"),
    formatSelect: $("#formatSelect"),
    captionSelect: $("#captionSelect"),
    voiceSelect: $("#voiceSelect"),
    formatBadge: $("#formatBadge"),
    previewFrame: $("#previewFrame"),
    previewPlaceholder: $("#previewPlaceholder"),
    stageImage: $("#stageImage"),
    stageCaption: $("#stageCaption"),
    renderCanvas: $("#renderCanvas"),
    resultVideo: $("#resultVideo"),
    previewMessage: $("#previewMessage"),
    resultActions: $("#resultActions"),
    playButton: $("#playButton"),
    speakButton: $("#speakButton"),
    downloadButton: $("#downloadButton"),
    generateButton: $("#generateButton"),
    generationOverlay: $("#generationOverlay"),
    generationStatus: $("#generationStatus"),
    progressBar: $("#progressBar"),
    progressText: $("#progressText"),
    demoButton: $("#demoButton"),
    toast: $("#toast")
  };

  const state = {
    imageFile: null,
    imageUrl: "",
    image: null,
    scriptFile: null,
    resultUrl: "",
    generating: false,
    speaking: false,
    toastTimer: null
  };

  const formatConfig = {
    portrait: { width: 540, height: 960, label: "9:16" },
    landscape: { width: 960, height: 540, label: "16:9" },
    square: { width: 720, height: 720, label: "1:1" }
  };

  const validImageTypes = new Set(["image/jpeg", "image/png", "image/webp"]);
  const validScriptExtensions = new Set(["txt", "md", "rtf", "docx", "pdf"]);

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) return "Demo asset";
    if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  function getWords() {
    return els.scriptText.value.trim().match(/\S+/g) || [];
  }

  function visualDuration() {
    const words = getWords().length;
    return Math.min(12, Math.max(4, words / 2.35));
  }

  function showToast(message) {
    window.clearTimeout(state.toastTimer);
    els.toast.textContent = message;
    els.toast.classList.add("show");
    state.toastTimer = window.setTimeout(() => els.toast.classList.remove("show"), 3200);
  }

  function setPreviewMessage(title, detail) {
    els.previewMessage.innerHTML = `<strong>${escapeHtml(title)}</strong><span>${escapeHtml(detail)}</span>`;
  }

  function escapeHtml(value) {
    const node = document.createElement("div");
    node.textContent = String(value);
    return node.innerHTML;
  }

  function updateReadiness() {
    const imageReady = Boolean(state.image);
    const words = getWords();
    const scriptReady = words.length >= 2;
    const count = Number(imageReady) + Number(scriptReady);

    els.characterSection.classList.toggle("ready", imageReady);
    els.scriptSection.classList.toggle("ready", scriptReady);
    els.stepCount.textContent = `${count} / 2 ready`;
    els.wordCount.textContent = `${words.length} word${words.length === 1 ? "" : "s"}`;
    els.durationEstimate.textContent = words.length ? `~ ${Math.ceil(visualDuration())} sec` : "~ 0 sec";
    els.generateButton.disabled = count !== 2 || state.generating;

    if (!state.resultUrl) {
      if (count === 2) {
        setPreviewMessage("Ready to perform", "Your visual draft is ready to generate.");
      } else if (imageReady) {
        setPreviewMessage("Character added", "Now attach or paste your script.");
      } else if (scriptReady) {
        setPreviewMessage("Script ready", "Now add the face of your character.");
      } else {
        setPreviewMessage("Waiting for your assets", "Add a portrait and script to begin.");
      }
    }
  }

  function resetResult() {
    window.speechSynthesis?.cancel();
    state.speaking = false;
    if (state.resultUrl) URL.revokeObjectURL(state.resultUrl);
    state.resultUrl = "";
    els.resultVideo.pause();
    els.resultVideo.removeAttribute("src");
    els.resultVideo.load();
    els.resultVideo.hidden = true;
    els.resultActions.hidden = true;
    els.renderCanvas.hidden = true;
    els.playButton.innerHTML = '<svg><use href="#i-play"></use></svg>';
    if (state.image) {
      els.stageImage.hidden = false;
      els.stageCaption.hidden = els.captionSelect.value === "none" || !els.scriptText.value.trim();
      els.stageCaption.textContent = firstCaption(els.scriptText.value);
    }
    updateReadiness();
  }

  function firstCaption(text) {
    const clean = text.replace(/\s+/g, " ").trim();
    if (!clean) return "";
    const sentence = clean.match(/^.{1,78}?(?:[.!?](?:\s|$)|$)/)?.[0] || clean.slice(0, 78);
    return sentence.length < clean.length && !/[.!?]$/.test(sentence) ? `${sentence}…` : sentence;
  }

  function setupDropZone(zone, input, handler) {
    zone.addEventListener("click", () => input.click());
    zone.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        input.click();
      }
    });
    ["dragenter", "dragover"].forEach((type) => zone.addEventListener(type, (event) => {
      event.preventDefault();
      zone.classList.add("dragging");
    }));
    ["dragleave", "drop"].forEach((type) => zone.addEventListener(type, (event) => {
      event.preventDefault();
      zone.classList.remove("dragging");
    }));
    zone.addEventListener("drop", (event) => {
      const file = event.dataTransfer?.files?.[0];
      if (file) handler(file);
    });
    input.addEventListener("change", () => {
      const file = input.files?.[0];
      if (file) handler(file);
    });
  }

  async function handleImage(file, isDemo = false) {
    els.imageError.textContent = "";
    if (!isDemo && !validImageTypes.has(file.type)) {
      els.imageError.textContent = "Please choose a JPG, PNG or WEBP image.";
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      els.imageError.textContent = "That image is over 15 MB. Please choose a smaller one.";
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    try {
      const image = await loadImage(objectUrl);
      if (state.imageUrl) URL.revokeObjectURL(state.imageUrl);
      state.imageFile = file;
      state.imageUrl = objectUrl;
      state.image = image;
      els.imageThumb.src = objectUrl;
      els.stageImage.src = objectUrl;
      els.stageImage.hidden = false;
      els.previewPlaceholder.hidden = true;
      els.imageName.textContent = file.name || "Demo portrait.png";
      els.imageMeta.textContent = `${image.naturalWidth} × ${image.naturalHeight} · ${formatBytes(file.size)}`;
      els.imageEmpty.hidden = true;
      els.imageLoaded.hidden = false;
      resetResult();
    } catch (error) {
      URL.revokeObjectURL(objectUrl);
      els.imageError.textContent = "We could not read that image. Please try another file.";
    }
  }

  function loadImage(url) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = reject;
      image.src = url;
    });
  }

  function clearImage(event) {
    event?.stopPropagation();
    if (state.imageUrl) URL.revokeObjectURL(state.imageUrl);
    state.imageFile = null;
    state.imageUrl = "";
    state.image = null;
    els.imageInput.value = "";
    els.imageThumb.removeAttribute("src");
    els.stageImage.removeAttribute("src");
    els.stageImage.hidden = true;
    els.stageCaption.hidden = true;
    els.previewPlaceholder.hidden = false;
    els.imageEmpty.hidden = false;
    els.imageLoaded.hidden = true;
    resetResult();
  }

  async function handleScript(file) {
    els.scriptError.textContent = "";
    const extension = file.name.split(".").pop()?.toLowerCase() || "";
    if (!validScriptExtensions.has(extension)) {
      els.scriptError.textContent = "Use a TXT, MD, RTF, DOCX or PDF script file.";
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      els.scriptError.textContent = "That script is over 10 MB. Please choose a smaller file.";
      return;
    }

    els.scriptDrop.querySelector("strong").textContent = "Reading your script…";
    try {
      const text = await readScriptFile(file, extension);
      const cleaned = cleanExtractedText(text);
      if (!cleaned) throw new Error("No readable text found");
      state.scriptFile = file;
      els.scriptText.value = cleaned.slice(0, 8000);
      els.scriptType.textContent = extension.toUpperCase();
      els.scriptName.textContent = file.name;
      els.scriptMeta.textContent = `${formatBytes(file.size)} · ${getWords().length} words read`;
      els.scriptFile.hidden = false;
      els.scriptDrop.hidden = true;
      resetResult();
      showToast("Script read successfully");
    } catch (error) {
      console.error(error);
      els.scriptError.textContent = extension === "docx" || extension === "pdf"
        ? "We could not extract this file. Check your connection or paste the script below."
        : "We could not find readable text in that file.";
      els.scriptDrop.querySelector("strong").textContent = "Attach your script";
    }
  }

  function cleanExtractedText(text) {
    return String(text)
      .replace(/\r\n?/g, "\n")
      .replace(/[\t\f\v]+/g, " ")
      .replace(/ {2,}/g, " ")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  async function readScriptFile(file, extension) {
    if (["txt", "md"].includes(extension)) return file.text();
    if (extension === "rtf") return parseRtf(await file.text());

    if (extension === "docx") {
      await loadExternalScript("https://cdn.jsdelivr.net/npm/mammoth@1.8.0/mammoth.browser.min.js", "mammoth");
      const result = await window.mammoth.extractRawText({ arrayBuffer: await file.arrayBuffer() });
      return result.value;
    }

    if (extension === "pdf") {
      await loadExternalScript("https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js", "pdfjsLib");
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js";
      const pdf = await window.pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise;
      const pages = [];
      for (let index = 1; index <= pdf.numPages; index += 1) {
        const page = await pdf.getPage(index);
        const content = await page.getTextContent();
        pages.push(content.items.map((item) => item.str).join(" "));
      }
      return pages.join("\n\n");
    }

    return "";
  }

  function parseRtf(rtf) {
    return rtf
      .replace(/\\par[d]?/g, "\n")
      .replace(/\\'[0-9a-fA-F]{2}/g, (match) => String.fromCharCode(parseInt(match.slice(2), 16)))
      .replace(/\\u(-?\d+)\??/g, (_, value) => String.fromCharCode(Number(value) < 0 ? Number(value) + 65536 : Number(value)))
      .replace(/\\[a-zA-Z]+-?\d* ?/g, "")
      .replace(/[{}]/g, "");
  }

  function loadExternalScript(src, globalName) {
    if (window[globalName]) return Promise.resolve();
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[data-library="${globalName}"]`);
      if (existing) {
        existing.addEventListener("load", resolve, { once: true });
        existing.addEventListener("error", reject, { once: true });
        return;
      }
      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.dataset.library = globalName;
      script.onload = resolve;
      script.onerror = () => reject(new Error(`Could not load ${globalName}`));
      document.head.appendChild(script);
    });
  }

  function clearScript(event) {
    event?.stopPropagation();
    state.scriptFile = null;
    els.scriptInput.value = "";
    els.scriptText.value = "";
    els.scriptFile.hidden = true;
    els.scriptDrop.hidden = false;
    els.scriptDrop.querySelector("strong").textContent = "Attach your script";
    els.scriptError.textContent = "";
    resetResult();
  }

  function changeFormat() {
    const format = els.formatSelect.value;
    els.previewFrame.classList.remove("portrait", "landscape", "square");
    els.previewFrame.classList.add(format);
    els.formatBadge.textContent = formatConfig[format].label;
    resetResult();
  }

  function populateVoices() {
    if (!("speechSynthesis" in window)) {
      els.voiceSelect.innerHTML = '<option value="">Voice unavailable</option>';
      els.voiceSelect.disabled = true;
      return;
    }
    const selected = els.voiceSelect.value;
    const voices = window.speechSynthesis.getVoices()
      .filter((voice) => /^en([-_]|$)/i.test(voice.lang))
      .slice(0, 20);
    els.voiceSelect.innerHTML = '<option value="">System voice</option>' + voices.map((voice) =>
      `<option value="${escapeHtml(voice.name)}">${escapeHtml(voice.name.replace(/\s*\([^)]*\)\s*/g, ""))}</option>`
    ).join("");
    if (voices.some((voice) => voice.name === selected)) els.voiceSelect.value = selected;
  }

  async function generateVideo() {
    if (!state.image || getWords().length < 2 || state.generating) return;
    if (!("MediaRecorder" in window) || !els.renderCanvas.captureStream) {
      showToast("Video export is not supported in this browser. Try Chrome or Edge.");
      return;
    }

    resetResult();
    state.generating = true;
    els.generateButton.disabled = true;
    els.generationOverlay.hidden = false;
    els.progressBar.style.width = "2%";
    els.progressText.textContent = "2%";
    els.generationStatus.textContent = "Preparing your character…";

    try {
      await new Promise((resolve) => window.setTimeout(resolve, 450));
      const blob = await recordCanvasVideo();
      state.resultUrl = URL.createObjectURL(blob);
      els.resultVideo.src = state.resultUrl;
      els.downloadButton.href = state.resultUrl;
      els.downloadButton.download = `persona-${Date.now()}.webm`;
      els.progressBar.style.width = "100%";
      els.progressText.textContent = "100%";
      els.generationStatus.textContent = "Your video is ready";
      await new Promise((resolve) => window.setTimeout(resolve, 600));

      els.renderCanvas.hidden = true;
      els.stageImage.hidden = true;
      els.stageCaption.hidden = true;
      els.resultVideo.hidden = false;
      els.resultActions.hidden = false;
      setPreviewMessage("Visual draft complete", `${Math.ceil(visualDuration())} sec · ${formatConfig[els.formatSelect.value].label} · WEBM`);
      showToast("Your video is ready to preview");
    } catch (error) {
      console.error(error);
      showToast("Something interrupted the export. Please try again.");
      els.stageImage.hidden = false;
    } finally {
      state.generating = false;
      els.generationOverlay.hidden = true;
      updateReadiness();
    }
  }

  function supportedMimeType() {
    const types = [
      "video/webm;codecs=vp9",
      "video/webm;codecs=vp8",
      "video/webm"
    ];
    return types.find((type) => MediaRecorder.isTypeSupported(type)) || "";
  }

  function recordCanvasVideo() {
    const config = formatConfig[els.formatSelect.value];
    const canvas = els.renderCanvas;
    const context = canvas.getContext("2d", { alpha: false });
    canvas.width = config.width;
    canvas.height = config.height;
    canvas.hidden = false;

    const stream = canvas.captureStream(24);
    const mimeType = supportedMimeType();
    const options = { videoBitsPerSecond: config.width > 800 ? 5_000_000 : 3_500_000 };
    if (mimeType) options.mimeType = mimeType;
    const recorder = new MediaRecorder(stream, options);
    const chunks = [];
    const duration = visualDuration();
    const captions = makeCaptionChunks(els.scriptText.value, els.formatSelect.value === "landscape" ? 13 : 9);

    return new Promise((resolve, reject) => {
      let animationFrame = 0;
      let stopped = false;
      const start = performance.now();

      recorder.ondataavailable = (event) => {
        if (event.data.size) chunks.push(event.data);
      };
      recorder.onerror = (event) => {
        stopped = true;
        window.cancelAnimationFrame(animationFrame);
        reject(event.error || new Error("Recorder error"));
      };
      recorder.onstop = () => {
        stopped = true;
        window.cancelAnimationFrame(animationFrame);
        stream.getTracks().forEach((track) => track.stop());
        resolve(new Blob(chunks, { type: mimeType || "video/webm" }));
      };

      function frame(now) {
        if (stopped) return;
        const elapsed = (now - start) / 1000;
        const progress = Math.min(1, elapsed / duration);
        drawVideoFrame(context, canvas, progress, captions);
        updateGenerationProgress(progress);
        if (progress >= 1) {
          recorder.requestData();
          recorder.stop();
          return;
        }
        animationFrame = window.requestAnimationFrame(frame);
      }

      try {
        recorder.start(500);
        animationFrame = window.requestAnimationFrame(frame);
      } catch (error) {
        reject(error);
      }
    });
  }

  function updateGenerationProgress(progress) {
    const value = Math.min(98, Math.round(8 + progress * 90));
    els.progressBar.style.width = `${value}%`;
    els.progressText.textContent = `${value}%`;
    if (progress < .18) els.generationStatus.textContent = "Composing the scene…";
    else if (progress < .58) els.generationStatus.textContent = "Animating your character…";
    else if (progress < .84) els.generationStatus.textContent = "Timing the captions…";
    else els.generationStatus.textContent = "Finishing your video…";
  }

  function makeCaptionChunks(text, maxWords) {
    const sentences = text.replace(/\s+/g, " ").trim().match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [text];
    const chunks = [];
    sentences.forEach((sentence) => {
      const words = sentence.trim().split(/\s+/);
      for (let index = 0; index < words.length; index += maxWords) {
        chunks.push(words.slice(index, index + maxWords).join(" "));
      }
    });
    return chunks.length ? chunks : [""];
  }

  function drawVideoFrame(context, canvas, progress, captions) {
    const { width, height } = canvas;
    const image = state.image;
    const slowPulse = Math.sin(progress * Math.PI * 3);
    const zoom = 1.035 + progress * .055 + slowPulse * .004;
    const driftX = Math.sin(progress * Math.PI * 1.7) * width * .012;
    const driftY = Math.sin(progress * Math.PI * 2.2) * height * .008;

    context.fillStyle = "#1a1b19";
    context.fillRect(0, 0, width, height);

    context.save();
    context.filter = "blur(28px) brightness(0.48) saturate(0.9)";
    context.globalAlpha = .94;
    drawCover(context, image, -35, -35, width + 70, height + 70, 1.16, driftX * -.3, driftY * -.3);
    context.restore();

    context.save();
    const sideInset = els.formatSelect.value === "landscape" ? width * .18 : 0;
    if (sideInset) {
      context.beginPath();
      context.roundRect(sideInset, 0, width - sideInset * 2, height, 18);
      context.clip();
      drawCover(context, image, sideInset, 0, width - sideInset * 2, height, zoom, driftX, driftY);
    } else {
      drawCover(context, image, 0, 0, width, height, zoom, driftX, driftY);
    }
    context.restore();

    const shade = context.createLinearGradient(0, height * .28, 0, height);
    shade.addColorStop(0, "rgba(0,0,0,0)");
    shade.addColorStop(.66, "rgba(0,0,0,.10)");
    shade.addColorStop(1, "rgba(0,0,0,.78)");
    context.fillStyle = shade;
    context.fillRect(0, 0, width, height);

    context.fillStyle = "rgba(255,255,255,.78)";
    context.font = `500 ${Math.max(8, Math.round(width * .012))}px DM Mono, monospace`;
    context.letterSpacing = `${Math.max(1, width * .002)}px`;
    context.fillText("PERSONA", width * .055, height * .055);
    context.fillStyle = "#ff5b35";
    context.beginPath();
    context.arc(width * .055 + context.measureText("PERSONA").width + width * .016, height * .051, Math.max(3, width * .004), 0, Math.PI * 2);
    context.fill();

    if (els.captionSelect.value !== "none") {
      const captionIndex = Math.min(captions.length - 1, Math.floor(progress * captions.length));
      drawCaption(context, canvas, captions[captionIndex], els.captionSelect.value);
    }

    context.fillStyle = "rgba(255,255,255,.24)";
    context.fillRect(width * .055, height * .952, width * .89, Math.max(2, height * .003));
    context.fillStyle = "#dfff64";
    context.fillRect(width * .055, height * .952, width * .89 * progress, Math.max(2, height * .003));
  }

  function drawCover(context, image, x, y, width, height, scale = 1, shiftX = 0, shiftY = 0) {
    const imageRatio = image.naturalWidth / image.naturalHeight;
    const targetRatio = width / height;
    let drawWidth;
    let drawHeight;
    if (imageRatio > targetRatio) {
      drawHeight = height * scale;
      drawWidth = drawHeight * imageRatio;
    } else {
      drawWidth = width * scale;
      drawHeight = drawWidth / imageRatio;
    }
    const drawX = x + (width - drawWidth) / 2 + shiftX;
    const drawY = y + (height - drawHeight) * .28 + shiftY;
    context.drawImage(image, drawX, drawY, drawWidth, drawHeight);
  }

  function drawCaption(context, canvas, text, style) {
    const { width, height } = canvas;
    const isLandscape = width > height;
    const maxWidth = width * (isLandscape ? .58 : .82);
    const fontSize = Math.round(width * (isLandscape ? .035 : .053));
    const lineHeight = fontSize * 1.22;
    const content = style === "bold" ? text.toUpperCase() : text;
    context.font = `${style === "bold" ? 800 : 700} ${fontSize}px Manrope, sans-serif`;
    context.textAlign = "center";
    context.textBaseline = "middle";
    const lines = wrapText(context, content, maxWidth);
    const centerY = height * (isLandscape ? .79 : .82);
    const boxHeight = lines.length * lineHeight + fontSize * .95;

    if (style === "minimal") {
      context.fillStyle = "rgba(13,14,12,.72)";
      roundRect(context, (width - maxWidth - fontSize) / 2, centerY - boxHeight / 2, maxWidth + fontSize, boxHeight, fontSize * .38);
      context.fill();
    }

    lines.forEach((line, index) => {
      const y = centerY + (index - (lines.length - 1) / 2) * lineHeight;
      context.lineWidth = Math.max(3, fontSize * .13);
      context.strokeStyle = "rgba(0,0,0,.58)";
      context.strokeText(line, width / 2, y);
      context.fillStyle = style === "bold" ? "#dfff64" : "#ffffff";
      context.fillText(line, width / 2, y);
    });
  }

  function wrapText(context, text, maxWidth) {
    const words = text.split(/\s+/);
    const lines = [];
    let line = "";
    words.forEach((word) => {
      const test = line ? `${line} ${word}` : word;
      if (line && context.measureText(test).width > maxWidth) {
        lines.push(line);
        line = word;
      } else {
        line = test;
      }
    });
    if (line) lines.push(line);
    return lines.slice(0, 4);
  }

  function roundRect(context, x, y, width, height, radius) {
    if (typeof context.roundRect === "function") {
      context.beginPath();
      context.roundRect(x, y, width, height, radius);
      return;
    }
    const r = Math.min(radius, width / 2, height / 2);
    context.beginPath();
    context.moveTo(x + r, y);
    context.arcTo(x + width, y, x + width, y + height, r);
    context.arcTo(x + width, y + height, x, y + height, r);
    context.arcTo(x, y + height, x, y, r);
    context.arcTo(x, y, x + width, y, r);
    context.closePath();
  }

  function toggleVideo() {
    if (!state.resultUrl) return;
    if (els.resultVideo.paused || els.resultVideo.ended) els.resultVideo.play();
    else els.resultVideo.pause();
  }

  function updatePlayIcon() {
    const icon = els.resultVideo.paused ? "play" : "pause";
    els.playButton.innerHTML = `<svg><use href="#i-${icon}"></use></svg>`;
    els.playButton.setAttribute("aria-label", els.resultVideo.paused ? "Play video" : "Pause video");
  }

  function toggleVoicePreview() {
    if (!("speechSynthesis" in window)) {
      showToast("Voice preview is not available in this browser.");
      return;
    }
    if (state.speaking) {
      window.speechSynthesis.cancel();
      state.speaking = false;
      els.speakButton.style.background = "";
      return;
    }

    const utterance = new SpeechSynthesisUtterance(els.scriptText.value.trim());
    const selectedName = els.voiceSelect.value;
    const voice = window.speechSynthesis.getVoices().find((item) => item.name === selectedName);
    if (voice) utterance.voice = voice;
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.onend = utterance.onerror = () => {
      state.speaking = false;
      els.speakButton.style.background = "";
    };
    state.speaking = true;
    els.speakButton.style.background = "#3c4038";
    if (state.resultUrl) {
      els.resultVideo.currentTime = 0;
      els.resultVideo.play().catch(() => {});
    }
    window.speechSynthesis.speak(utterance);
  }

  async function loadDemo() {
    if (state.generating) return;
    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200" viewBox="0 0 900 1200">
        <rect width="900" height="1200" fill="#d8cab9"/>
        <circle cx="760" cy="180" r="260" fill="#f15f3a" opacity=".82"/>
        <path d="M0 880 Q280 715 565 845 T900 785 V1200 H0Z" fill="#637e78"/>
        <ellipse cx="454" cy="548" rx="226" ry="280" fill="#815438"/>
        <path d="M238 508c8-216 92-337 224-337 158 0 239 130 233 339-59-31-89-100-102-168-100 86-221 126-355 131z" fill="#29211e"/>
        <ellipse cx="448" cy="560" rx="185" ry="226" fill="#a96f4b"/>
        <path d="M269 514c29-1 79-18 121-44 77-46 132-85 190-150 29 54 56 107 72 181-59-23-98-64-113-105-67 65-158 109-270 118z" fill="#29211e"/>
        <ellipse cx="368" cy="568" rx="19" ry="13" fill="#171816"/>
        <ellipse cx="533" cy="568" rx="19" ry="13" fill="#171816"/>
        <path d="M418 673q39 33 82 0" fill="none" stroke="#5d2d27" stroke-width="13" stroke-linecap="round"/>
        <path d="M431 578q-15 69-3 87h39" fill="none" stroke="#875136" stroke-width="10" stroke-linecap="round"/>
        <path d="M314 516q52-35 101-1M495 513q49-30 96 6" fill="none" stroke="#4c3026" stroke-width="13" stroke-linecap="round"/>
        <path d="M303 787q143 107 295 0l70 52c103 77 146 208 162 361H70c21-185 69-303 174-362z" fill="#202526"/>
        <path d="M360 786q91 70 180 0l-13 126-77 70-79-71z" fill="#966044"/>
        <circle cx="145" cy="150" r="68" fill="#dfff64"/>
        <path d="M113 153l24 24 43-53" fill="none" stroke="#202526" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`;
    const file = new File([new Blob([svg], { type: "image/svg+xml" })], "amara-demo-portrait.svg", { type: "image/svg+xml" });
    await handleImage(file, true);
    state.scriptFile = null;
    els.scriptInput.value = "";
    els.scriptFile.hidden = true;
    els.scriptDrop.hidden = false;
    els.scriptText.value = "Every idea starts as a quiet possibility. Give it a voice, a face, and a moment to be heard. Your story is ready. Let’s bring it to life.";
    resetResult();
    showToast("Demo project loaded — ready to generate");
    document.querySelector(".studio").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  setupDropZone(els.imageDrop, els.imageInput, handleImage);
  setupDropZone(els.scriptDrop, els.scriptInput, handleScript);
  els.removeImage.addEventListener("click", clearImage);
  els.removeScript.addEventListener("click", clearScript);
  els.scriptFile.addEventListener("click", (event) => event.stopPropagation());
  els.scriptText.addEventListener("input", () => {
    els.scriptError.textContent = "";
    resetResult();
  });
  els.formatSelect.addEventListener("change", changeFormat);
  els.captionSelect.addEventListener("change", resetResult);
  els.generateButton.addEventListener("click", generateVideo);
  els.playButton.addEventListener("click", toggleVideo);
  els.speakButton.addEventListener("click", toggleVoicePreview);
  els.resultVideo.addEventListener("play", updatePlayIcon);
  els.resultVideo.addEventListener("pause", updatePlayIcon);
  els.resultVideo.addEventListener("ended", updatePlayIcon);
  els.demoButton.addEventListener("click", loadDemo);
  window.addEventListener("beforeunload", () => {
    if (state.imageUrl) URL.revokeObjectURL(state.imageUrl);
    if (state.resultUrl) URL.revokeObjectURL(state.resultUrl);
    window.speechSynthesis?.cancel();
  });

  if ("speechSynthesis" in window) {
    populateVoices();
    window.speechSynthesis.addEventListener?.("voiceschanged", populateVoices);
    window.speechSynthesis.onvoiceschanged = populateVoices;
  } else {
    populateVoices();
  }
  changeFormat();
  updateReadiness();
})();
