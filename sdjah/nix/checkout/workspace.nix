{ pkgs, uv2nix, pyproject-nix, pyproject-build-systems }:

let
  # Choose your Python version
  python = pkgs.python312;

  # Any external dependencies to bring into the final environment:
  dependencies = [ python pkgs.postgresql_17 pkgs.google-chrome ];

  # 1) Load your local Python workspace
  workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ../../.; };

  # 2) Create an overlay from your Python project
  baseOverlay = workspace.mkPyprojectOverlay { sourcePreference = "wheel"; };

  # 3) Here are your build system overrides:
  buildSystemOverrides = {
    cdp-socket = { setuptools = [ ]; };
    psycopg2-binary = { setuptools = [ ]; };
    psycopg2 = { setuptools = [ ]; };
  };

  # 4) Our function that applies the above overrides.
  #    This will also add xsimd, plus the trick to provide a fake pkg-config for xsimd.
  applyBuildSystemOverrides = final: prev:
    let
      inherit (final) resolveBuildSystem;
      inherit (builtins) mapAttrs;
    in mapAttrs (name: spec:
      prev.${name}.overrideAttrs (old: {
        nativeBuildInputs = old.nativeBuildInputs ++ resolveBuildSystem spec;
        buildInputs = (old.buildInputs or [ ])
          ++ [ pkgs.postgresql_17 pkgs.openssl ];
      })) buildSystemOverrides;

  # applyBuildSystemOverrides = final: prev:
  #   let inherit (final) resolveBuildSystem;
  #   in builtins.mapAttrs (name: spec:
  #     prev.${name}.overrideAttrs (old: {
  #       buildInputs = (old.buildInputs or [ ])
  #         ++ [ pkgs.postgresql_17 pkgs.openssl ];
  #     })) buildSystemOverrides;

  # 5) Combine our overrides with any from pyproject-build-systems
  pyprojectOverrides = final: prev:
    let overriddenPackages = applyBuildSystemOverrides final prev;
    in prev // overriddenPackages;

  # 6) Construct your Python set, but with an stdenv override for Ventura 13.3
  #    (MacOS SDK version 15.1 => Darwin version 24).
  pythonSet = (pkgs.callPackage pyproject-nix.build.packages {
    inherit python;

    # Here is where we override the stdenv for Ventura 13.3
    stdenv = pkgs.stdenv.override {
      targetPlatform = pkgs.stdenv.targetPlatform // {
        # Sets MacOS SDK version to 15.1
        darwinSdkVersion = "15.1";
      };
    };
  }).overrideScope (pkgs.lib.composeManyExtensions [
    pyproject-build-systems.overlays.default # standard pyproject-nix build-systems
    baseOverlay # your local project overlay
    pyprojectOverrides # the function that adds xsimd & overrides
  ]);

in { inherit pythonSet workspace dependencies python; }
