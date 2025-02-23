{ pkgs }: {
  deps = [
    pkgs.ffmpeg-full
    pkgs.ffmpeg
    pkgs.python311
    pkgs.python311Packages.pip
  ];
}
