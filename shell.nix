with import <nixpkgs> {};

let

  bidict = with python34Packages; buildPythonPackage rec {
    name = "bidict-0.13.0";
    src = fetchurl {
      url = "mirror://pypi/b/bidict/bidict-0.13.0.tar.gz";
      sha256 = "150y85nrxdkqvij3s7rvq4xz2cb7qba5g25n0divp83bjzy3jwkq";
    };
    doCheck = false;
  };

  stem = with python34Packages; buildPythonPackage rec {
    name = "stem-1.5.4";
    src = fetchurl {
      url = "mirror://pypi/s/stem/stem-1.5.4.tar.gz";
      sha256 = "1j7pnblrn0yr6jmxvsq6y0ihmxmj5x50jl2n2606w67f6wq16j9n";
    };
    buildInputs = lib.optional (!stdenv.isDarwin) tor;
    propagatedBuildInputs = [ mock pyflakes pycodestyle pycrypto tox ];
  };

in stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    python34
    python34Packages.pysocks
    python34Packages.requests2
    bidict
    stem
  ] ++ lib.optional (!stdenv.isDarwin) tor;
  shellHook = ''
    export PYTHONPATH=.:$PYTHONPATH
  '';
}
