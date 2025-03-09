{ pkgs, uv2nixSet }:

let
  editableOverlay =
    uv2nixSet.workspace.mkEditablePyprojectOverlay { root = "$REPO_ROOT"; };

  editablePythonSet = uv2nixSet.pythonSet.overrideScope
    (pkgs.lib.composeManyExtensions [
      editableOverlay
      # Apply fixups for building an editable package of your workspace packages
      (final: prev: {
        checkout = prev.checkout.overrideAttrs (old: {
          nativeBuildInputs = old.nativeBuildInputs
            ++ final.resolveBuildSystem { editables = [ ]; };
        });
      })
    ]);

  localVenv = editablePythonSet.mkVirtualEnv "checkout" {
    inherit (uv2nixSet.workspace.deps.all) checkout;
  };

in pkgs.mkShell {
  packages = [ localVenv pkgs.git pkgs.uv ] ++ uv2nixSet.dependencies;

  shellHook = ''
    unset PYTHONPATH
    export UV_NO_SYNC=1
    export DISPLAY=:0
    export UV_PYTHON_DOWNLOADS=never
    export REPO_ROOT=$(git rev-parse --show-toplevel)
    set -a && source .env && set +a
  '';
}
