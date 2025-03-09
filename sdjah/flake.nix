{
  description = "PoC Caliente scraping";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, uv2nix, pyproject-nix, pyproject-build-systems }:
    let

      inherit (nixpkgs) lib;

      system = "aarch64-darwin";
      pkgs = import nixpkgs {
        system = system;
        config.allowUnfree = true;
      };

      ####################################################
      ## UV2NIX
      ####################################################
      # Load our Python environment, jars, overlays, etc.
      eatSet = import ./nix/workspace.nix {
        inherit pkgs uv2nix pyproject-nix pyproject-build-systems;
      };

      # Import DevShell
      eatsDevshell = import ./nix/devshell.nix {
        inherit pkgs;
        uv2nixSet = eatSet;
      };


    in {
      devShells.aarch64-darwin = {
        default = eatsDevshell;
        # checkout = checkoutDevshell;
      };

    };
}
