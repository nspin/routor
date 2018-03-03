with import <nixpkgs> {};

let

  bidict = with python3Packages; buildPythonPackage rec {
    name = "bidict-0.13.0";
    src = fetchurl {
      url = "mirror://pypi/b/bidict/bidict-0.13.0.tar.gz";
      sha256 = "150y85nrxdkqvij3s7rvq4xz2cb7qba5g25n0divp83bjzy3jwkq";
    };
    doCheck = false;
  };

  stem = with python3Packages; buildPythonPackage rec {
    name = "stem-1.6.0";
    src = fetchurl {
      url = "mirror://pypi/s/stem/${name}.tar.gz";
      sha256 = "1va9p3ij7lxg6ixfsvaql06dn11l3fgpxmss1dhlvafm7sqizznp";
    };
    doCheck = false;
    buildInputs = lib.optional (!stdenv.isDarwin) tor;
    propagatedBuildInputs = [ mock pyflakes pycodestyle pycrypto tox ];
  };

in stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    python3
    python3Packages.requests
    bidict
    stem
  ] ++ lib.optional (!stdenv.isDarwin) tor;
  shellHook = ''
    export PYTHONPATH=.:$PYTHONPATH
  '';
}
