import type { ReactNode } from 'react';
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import styled from 'styled-components';

// ---------------------------------------------------------------------------
// Composition constants
// ---------------------------------------------------------------------------

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;

const sec = (n: number) => Math.round(n * FPS);

const S1_DURATION = sec(4.5); // 135
const S2_DURATION = sec(7); // 210
const S3_DURATION = sec(7); // 210
const S4_DURATION = sec(7); // 210
const S5_DURATION = sec(7.5); // 225

const S1_FROM = 0;
const S2_FROM = S1_FROM + S1_DURATION;
const S3_FROM = S2_FROM + S2_DURATION;
const S4_FROM = S3_FROM + S3_DURATION;
const S5_FROM = S4_FROM + S4_DURATION;

export const TOTAL_DURATION = S5_FROM + S5_DURATION; // 990 frames = 33s

// ---------------------------------------------------------------------------
// Shared styles
// ---------------------------------------------------------------------------

const PhoneScreen = styled.div`
  width: 1080px;
  height: 1920px;
  background: #000;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'DejaVu Sans', Helvetica, sans-serif;
  position: relative;
  overflow: hidden;
`;

const StatusBar = styled.div`
  height: 100px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 60px;
  font-size: 42px;
  font-weight: 600;
  z-index: 100;
  position: absolute;
  top: 0;
`;

const CVPaper = styled.div`
  width: 900px;
  min-height: 1500px;
  background: #fdfdfd;
  color: #1a1a1a;
  margin: 120px auto;
  padding: 60px;
  font-family: 'DejaVu Serif', 'Times New Roman', Georgia, serif;
  font-size: 32px;
  line-height: 1.4;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
  position: relative;
  overflow: hidden;
`;

const Toast = styled.div`
  position: absolute;
  bottom: 200px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(30, 30, 30, 0.92);
  color: white;
  padding: 28px 54px;
  border-radius: 44px;
  font-size: 40px;
  font-weight: 600;
  z-index: 1000;
`;

// ---------------------------------------------------------------------------
// Small building blocks
// ---------------------------------------------------------------------------

const Battery = () => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
    <span>84%</span>
    <div
      style={{
        width: 56,
        height: 28,
        border: '2px solid white',
        borderRadius: 7,
        padding: 3,
        display: 'inline-flex',
      }}
    >
      <div
        style={{
          width: '84%',
          height: '100%',
          background: 'white',
          borderRadius: 3,
        }}
      />
    </div>
    <div
      style={{
        width: 4,
        height: 12,
        background: 'white',
        borderRadius: '0 3px 3px 0',
        marginLeft: -10,
      }}
    />
  </div>
);

const CheckIcon = ({
  size = 30,
  color = '#ffffff',
  strokeWidth = 3.5,
}: {
  size?: number;
  color?: string;
  strokeWidth?: number;
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M4 12.5 L9 17.5 L20 6.5"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const DoubleCheck = ({ size = 30, color = '#53bdeb' }: { size?: number; color?: string }) => (
  <div style={{ display: 'flex', marginRight: 8 }}>
    <svg width={size} height={size} viewBox="0 0 30 24" fill="none" style={{ marginRight: -8 }}>
      <path
        d="M2 12.5 L8 18.5 L17 7.5"
        stroke={color}
        strokeWidth={3.5}
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
    <svg width={size} height={size} viewBox="0 0 30 24" fill="none">
      <path
        d="M2 12.5 L8 18.5 L17 7.5"
        stroke={color}
        strokeWidth={3.5}
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  </div>
);

// ---------------------------------------------------------------------------
// Scene 1 — "This is not a CV."
// ---------------------------------------------------------------------------

const SENSITIVE_FIELDS = [
  'ID number: 900314 0081 085',
  'Race: Black',
  'Marital status: Single',
  'Dependants: 2',
  'Religion: Zion',
  'Address: 14 Mkhize St, Tembisa',
];

const SensitiveLine = ({ text, frame, index }: { text: string; frame: number; index: number }) => {
  const from = 30 + index * 10;
  const opacity = interpolate(frame, [from, from + 12], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const x = interpolate(frame, [from, from + 12], [40, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        background: 'rgba(220, 38, 38, 0.08)',
        borderLeft: '6px solid #dc2626',
        padding: '8px 18px',
        margin: '6px 0',
        borderRadius: '0 8px 8px 0',
        opacity,
        transform: `translateX(${x}px)`,
      }}
    >
      {text}
    </div>
  );
};

const Scene1_NotACV = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const paperY = interpolate(frame, [0, 22], [80, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const paperOpacity = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const nameOpacity = interpolate(frame, [18, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const toastScale = spring({
    frame: frame - 70,
    fps,
    config: { damping: 12, stiffness: 160 },
  });
  const toastOpacity = interpolate(frame, [70, 78], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <PhoneScreen>
      <StatusBar>
        <span>19:42</span>
        <Battery />
      </StatusBar>

      <div
        style={{
          transform: `translateY(${paperY}px)`,
          opacity: paperOpacity,
        }}
      >
        <CVPaper>
          <h1
            style={{
              fontSize: 52,
              fontWeight: 'bold',
              marginBottom: 26,
              opacity: nameOpacity,
            }}
          >
            THANDI NKOSI
          </h1>

          {SENSITIVE_FIELDS.map((text, i) => (
            <SensitiveLine key={text} text={text} frame={frame} index={i} />
          ))}

          <div style={{ marginTop: 90, borderTop: '1px solid #ccc', paddingTop: 20 }}>
            <p style={{ fontWeight: 'bold' }}>WORK EXPERIENCE</p>
            <p>Retail Assistant — 2021–2024 …</p>
          </div>
        </CVPaper>
      </div>

      {frame >= 70 && (
        <Toast style={{ transform: `translateX(-50%) scale(${Math.max(toastScale, 0)})`, opacity: toastOpacity }}>
          This is not a CV.
        </Toast>
      )}
    </PhoneScreen>
  );
};

// ---------------------------------------------------------------------------
// Scene 2 — WhatsApp
// ---------------------------------------------------------------------------

const Scene2_WhatsApp = () => {
  const frame = useCurrentFrame();

  const typingDots = [0, 1, 2].map((i) => {
    const bounce = -Math.max(0, Math.sin((frame - i * 5) * 0.45)) * 8;
    return bounce;
  });

  const typingOpacity = interpolate(frame, [10, 20, 48, 56], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const msgY = interpolate(frame, [50, 64], [40, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const msgOpacity = interpolate(frame, [50, 62], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const replyY = interpolate(frame, [110, 124], [50, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const replyOpacity = interpolate(frame, [110, 122], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const seenOpacity = interpolate(frame, [150, 162], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const captionOpacity = interpolate(frame, [182, 202], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <PhoneScreen style={{ background: '#0B141A' }}>
      <StatusBar>
        <span>19:42</span>
        <Battery />
      </StatusBar>

      {/* WhatsApp header */}
      <div
        style={{
          background: '#202C33',
          height: 160,
          display: 'flex',
          alignItems: 'center',
          padding: '0 30px',
          marginTop: 100,
        }}
      >
        <div
          style={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            background: '#6a7b86',
            marginRight: 20,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 40,
            fontWeight: 'bold',
            color: '#0B141A',
          }}
        >
          T
        </div>
        <div>
          <div style={{ fontSize: 36, fontWeight: 'bold' }}>Recruiter · Thabo</div>
          <div style={{ fontSize: 24, color: '#8696a0' }}>online</div>
        </div>
      </div>

      {/* Chat area */}
      <div style={{ padding: '40px', position: 'relative' }}>
        {frame < 50 && (
          <div
            style={{
              background: '#202C33',
              padding: '20px 26px',
              borderRadius: '14px',
              width: 120,
              marginBottom: 30,
              opacity: typingOpacity,
              display: 'flex',
              gap: 12,
              justifyContent: 'center',
            }}
          >
            {typingDots.map((y, i) => (
              <div
                key={i}
                style={{
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  background: '#8696a0',
                  transform: `translateY(${y}px)`,
                }}
              />
            ))}
          </div>
        )}

        <div
          style={{
            background: '#202C33',
            padding: '22px',
            borderRadius: '14px',
            width: '78%',
            marginBottom: 30,
            fontSize: 32,
            transform: `translateY(${msgY}px)`,
            opacity: msgOpacity,
          }}
        >
          Hi Thandi — please send your CV, certified ID and proof of address today.
        </div>

        <div
          style={{
            background: '#005C4B',
            padding: '16px',
            borderRadius: '14px',
            width: '74%',
            marginLeft: 'auto',
            fontSize: 32,
            transform: `translateY(${replyY}px)`,
            opacity: replyOpacity,
          }}
        >
          <div
            style={{
              background: '#d1d5db',
              color: '#000',
              padding: '14px 18px',
              borderRadius: '10px',
              display: 'flex',
              alignItems: 'center',
              gap: 14,
            }}
          >
            <span
              style={{
                background: '#dc2626',
                color: '#fff',
                borderRadius: '6px',
                padding: '4px 12px',
                fontWeight: 700,
                fontSize: 24,
                letterSpacing: 1,
              }}
            >
              PDF
            </span>
            <span>Thandi_CV_FINAL.pdf</span>
          </div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              marginTop: 6,
              fontSize: 22,
              color: '#8696a0',
              opacity: seenOpacity,
            }}
          >
            <span style={{ marginRight: 4 }}>Seen</span>
            <DoubleCheck size={26} />
          </div>
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 160,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontSize: 44,
          fontWeight: 700,
          color: '#fecaca',
          opacity: captionOpacity,
        }}
      >
        Her CV already says too much.
      </div>
    </PhoneScreen>
  );
};

// ---------------------------------------------------------------------------
// Scene 3 — Redaction slam
// ---------------------------------------------------------------------------

const RedactionBar = styled.div<{ progress: number }>`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: #0b0b0b;
  transform: ${(p) => `scaleX(${p.progress})`};
  transform-origin: left;
`;

const Scene3_Redaction = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bars = SENSITIVE_FIELDS.map((_, i) => {
    const start = 20 + i * 22;
    const progress = spring({
      frame: frame - start,
      fps,
      config: { damping: 15, stiffness: 210, mass: 0.9 },
    });
    return { start, progress };
  });

  const captionOpacity = interpolate(frame, [165, 185], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const captionY = interpolate(frame, [165, 185], [30, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <PhoneScreen>
      <StatusBar>
        <span>19:42</span>
        <Battery />
      </StatusBar>

      <CVPaper>
        <h1 style={{ fontSize: 48, fontWeight: 'bold', marginBottom: 10 }}>THANDI NKOSI</h1>
        <p style={{ fontSize: 26, color: '#555', marginBottom: 24 }}>
          thandi@email.com · 067 000 0000
        </p>

        {SENSITIVE_FIELDS.map((text, i) => (
          <div
            key={text}
            style={{
              position: 'relative',
              padding: '8px 18px',
              margin: '6px 0',
              borderRadius: 8,
            }}
          >
            <span>{text}</span>
            <RedactionBar progress={bars[i].progress} />
          </div>
        ))}

        <div style={{ marginTop: 90, borderTop: '1px solid #ccc', paddingTop: 20 }}>
          <p style={{ fontWeight: 'bold' }}>WORK EXPERIENCE</p>
          <p>Retail Assistant — 2021–2024 …</p>
        </div>
      </CVPaper>

      <div
        style={{
          position: 'absolute',
          bottom: 220,
          left: 60,
          right: 60,
          background: 'rgba(0, 0, 0, 0.85)',
          border: '2px solid rgba(255,255,255,0.15)',
          borderRadius: 28,
          padding: '40px 40px',
          textAlign: 'center',
          opacity: captionOpacity,
          transform: `translateY(${captionY}px)`,
        }}
      >
        <div style={{ fontSize: 60, fontWeight: 'bold', lineHeight: 1.15 }}>Real job. Asks later.</div>
        <div style={{ fontSize: 30, color: '#cbd5e1', marginTop: 12 }}>
          Your CV doesn’t need any of this.
        </div>
      </div>
    </PhoneScreen>
  );
};

// ---------------------------------------------------------------------------
// Scene 4 — This is a CV
// ---------------------------------------------------------------------------

const CleanSection = ({
  title,
  children,
  frame,
  from,
}: {
  title: string;
  children: ReactNode;
  frame: number;
  from: number;
}) => {
  const opacity = interpolate(frame, [from, from + 14], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(frame, [from, from + 14], [24, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ opacity, transform: `translateY(${y}px)`, marginBottom: 26 }}>
      <p style={{ fontWeight: 'bold', borderBottom: '2px solid #e5e7eb', paddingBottom: 6 }}>{title}</p>
      {children}
    </div>
  );
};

const Scene4_CleanCV = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bannerY = interpolate(frame, [0, 18], [-70, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const bannerOpacity = interpolate(frame, [0, 16], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const paperY = interpolate(frame, [18, 40], [120, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const paperOpacity = interpolate(frame, [18, 34], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const stripOpacity = interpolate(frame, [172, 190], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const stripY = interpolate(frame, [172, 190], [24, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const checkScale = spring({ frame: frame - 10, fps, config: { damping: 12, stiffness: 180 } });

  return (
    <PhoneScreen style={{ background: '#0e1419' }}>
      <StatusBar>
        <span>19:42</span>
        <Battery />
      </StatusBar>

      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 60,
          right: 60,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 22,
          opacity: bannerOpacity,
          transform: `translateY(${bannerY}px)`,
        }}
      >
        <span
          style={{
            width: 72,
            height: 72,
            borderRadius: '50%',
            background: '#16a34a',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            transform: `scale(${Math.max(checkScale, 0)})`,
          }}
        >
          <CheckIcon size={40} color="#fff" strokeWidth={4} />
        </span>
        <span style={{ fontSize: 64, fontWeight: 'bold' }}>This is a CV.</span>
      </div>

      <div style={{ transform: `translateY(${paperY}px)`, opacity: paperOpacity }}>
        <CVPaper style={{ marginTop: 320 }}>
          <h1 style={{ fontSize: 48, fontWeight: 'bold', marginBottom: 10 }}>THANDI NKOSI</h1>
          <p style={{ fontSize: 26, color: '#555', marginBottom: 30 }}>
            thandi@email.com · 067 000 0000 · LinkedIn/thandi-nkosi
          </p>

          <CleanSection title="PROFESSIONAL SUMMARY" frame={frame} from={46}>
            <p>Reliable retail assistant with 4+ years on the shop floor. Great with customers, honest with cash.</p>
          </CleanSection>

          <CleanSection title="SKILLS" frame={frame} from={60}>
            <p>Retail sales · POS &amp; cash handling · Stock control · Customer service · Excel</p>
          </CleanSection>

          <CleanSection title="WORK EXPERIENCE" frame={frame} from={74}>
            <p>Retail Assistant — Shoprite, Tembisa · 2021–2024</p>
            <p>Cashier — Boxer, Tembisa · 2019–2021</p>
          </CleanSection>

          <CleanSection title="EDUCATION" frame={frame} from={88}>
            <p>Matric (Grade 12) — 2018</p>
          </CleanSection>
        </CVPaper>
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 140,
          left: 60,
          right: 60,
          background: '#16a34a',
          borderRadius: 22,
          padding: '26px 30px',
          textAlign: 'center',
          fontSize: 34,
          fontWeight: 600,
          opacity: stripOpacity,
          transform: `translateY(${stripY}px)`,
        }}
      >
        No ID · No race · No religion · No home address
      </div>
    </PhoneScreen>
  );
};

// ---------------------------------------------------------------------------
// Scene 5 — Payoff
// ---------------------------------------------------------------------------

const PayoffItem = ({
  text,
  frame,
  from,
}: {
  text: string;
  frame: number;
  from: number;
}) => {
  const opacity = interpolate(frame, [from, from + 12], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const x = interpolate(frame, [from, from + 12], [-30, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 20,
        margin: '16px 0',
        opacity,
        transform: `translateX(${x}px)`,
      }}
    >
      <span
        style={{
          width: 46,
          height: 46,
          borderRadius: '50%',
          background: '#16a34a',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}
      >
        <CheckIcon size={26} color="#fff" strokeWidth={4} />
      </span>
      <span style={{ fontSize: 38 }}>{text}</span>
    </div>
  );
};

const Scene5_Payoff = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headOpacity = interpolate(frame, [8, 24], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const subOpacity = interpolate(frame, [22, 38], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const footerOpacity = interpolate(frame, [180, 200], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const fadeOut = interpolate(frame, [S5_DURATION - 20, S5_DURATION], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const checkScale = spring({ frame: frame - 45, fps, config: { damping: 12, stiffness: 160 } });

  return (
    <PhoneScreen style={{ background: '#0B1220' }}>
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          padding: '200px 90px 160px',
          boxSizing: 'border-box',
          display: 'flex',
          flexDirection: 'column',
          opacity: fadeOut,
        }}
      >
        <div style={{ fontSize: 92, fontWeight: 800, lineHeight: 1.08, opacity: headOpacity }}>
          Keep your CV clean.
        </div>
        <div style={{ fontSize: 44, color: '#C4A265', marginTop: 20, opacity: subOpacity }}>
          A real job asks later.
        </div>

        <div style={{ marginTop: 60 }}>
          <PayoffItem text="No ID number on the CV" frame={frame} from={50} />
          <PayoffItem text="No race, religion or marital status" frame={frame} from={64} />
          <PayoffItem text="No home address or dependants" frame={frame} from={78} />
          <PayoffItem text="Yes: skills, experience, contact" frame={frame} from={92} />
        </div>

        <div
          style={{
            marginTop: 'auto',
            borderTop: '2px solid rgba(255,255,255,0.12)',
            paddingTop: 40,
            display: 'flex',
            alignItems: 'center',
            gap: 20,
            opacity: footerOpacity,
          }}
        >
          <span
            style={{
              width: 64,
              height: 64,
              borderRadius: 18,
              background: '#C4A265',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              transform: `scale(${Math.max(checkScale, 0)})`,
            }}
          >
            <CheckIcon size={36} color="#0B1220" strokeWidth={4} />
          </span>
          <div>
            <div style={{ fontSize: 44, fontWeight: 700 }}>jobready.za</div>
            <div style={{ fontSize: 26, color: '#9aa7b4' }}>Your CV. Your info. Your call.</div>
          </div>
        </div>
      </div>
    </PhoneScreen>
  );
};

// ---------------------------------------------------------------------------
// Composition
// ---------------------------------------------------------------------------

export const JobReadyVideo = () => {
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      <Sequence from={S1_FROM} durationInFrames={S1_DURATION}>
        <Scene1_NotACV />
      </Sequence>
      <Sequence from={S2_FROM} durationInFrames={S2_DURATION}>
        <Scene2_WhatsApp />
      </Sequence>
      <Sequence from={S3_FROM} durationInFrames={S3_DURATION}>
        <Scene3_Redaction />
      </Sequence>
      <Sequence from={S4_FROM} durationInFrames={S4_DURATION}>
        <Scene4_CleanCV />
      </Sequence>
      <Sequence from={S5_FROM} durationInFrames={S5_DURATION}>
        <Scene5_Payoff />
      </Sequence>
    </AbsoluteFill>
  );
};
