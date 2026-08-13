import { Composition } from 'remotion';
import { JobReadyVideo, TOTAL_DURATION, FPS, WIDTH, HEIGHT } from './JobReadyVideo';

export const RemotionRoot = () => {
  return (
    <Composition
      id="JobReadyVideo"
      component={JobReadyVideo}
      durationInFrames={TOTAL_DURATION}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
