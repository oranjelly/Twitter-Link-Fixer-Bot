{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.openssl  # Required for HTTPS (secure connection to Discord)
  ];
}
