let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.pandas
      python-pkgs.requests
      python-pkgs.numpy
      python-pkgs.fastapi
      python-pkgs.pymongo
      python-pkgs.python-dotenv
      python-pkgs.openai
    ]))
  ];
}