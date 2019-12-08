from pathlib import Path
from os import system


wav_16khz = Path('/Users/dintu/work_sp/data/intel_wav')
feat_dir = Path('feat')
if 0:
    if not feat_dir.is_dir():
        feat_dir.mkdir()
    for i, wav_path in enumerate(wav_16khz.glob('*.wav')):
        print(wav_path)
        s16_name = wav_path.name.replace('.wav', '.s16')
        s16_path = feat_dir.joinpath(s16_name)
        
        s16_cmd = f"sox {wav_path} -r 16000 -c 1 -t sw {s16_path}"
        print(s16_cmd)
        system(s16_cmd)

        f32_name = wav_path.name.replace('.wav', '.f32')
        f32_path = feat_dir.joinpath(f32_name)
        f32_cmd = f"./dump_data -test {s16_path} {f32_path}"
        print(f32_cmd)
        if s16_path.is_file():
            system(f32_cmd)
        else:
            print(f"File not found {f32_path}")
        if i > 10: break
if 1:
    import numpy as np
    for i, feat_path in enumerate(feat_dir.glob('*.s16')):
        f32_name = feat_path.name.replace('.s16', '.f32')
        
        
        feats = np.fromfile(feat_dir.joinpath(f32_name), dtype='float32')
        feats = feats.reshape((-1, 55))
        print(feats.shape)

        real_feat = np.c_[feats[:,:18], feats[:,36:]]
        print(real_feat.shape)

        wav = np.fromfile(feat_path, dtype='int16')
       
        FRAME_SIZE = 160  # 10 ms
        OVERLAP_SIZE = 160  # 10 ms
        WINDOW_SIZE = OVERLAP_SIZE + FRAME_SIZE
        mem = np.zeros(OVERLAP_SIZE)
        wav_frames = []
        for i in range(len(wav)//FRAME_SIZE):
            frame = np.zeros(WINDOW_SIZE)
            frame[:OVERLAP_SIZE] = mem
            frame[OVERLAP_SIZE:] = wav[i*FRAME_SIZE:(i+1)*FRAME_SIZE]
            wav_frames.append(frame.reshape((1,-1)))
        wav_frames = np.concatenate(wav_frames)
        print(wav_frames.shape)
