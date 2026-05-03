"""
Template-pack validator tests for canon #11 — Seven Layer Architecture Template Pack.

Verifies:
  - README.md exists and has H1 heading
  - LICENSE exists and contains expected MIT terms + author
  - Both sub-template-packs (Phase + A2A/MCP) are present
  - Phase pack has 10 numbered template subdirectories
  - A2A/MCP pack has 6 numbered template subdirectories
  - No common junk (.pyc, __pycache__, .DS_Store) in repo root
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent


class TestRepoStructure:
    def test_readme_exists(self):
        assert (ROOT / "README.md").exists()

    def test_readme_nonempty(self):
        assert (ROOT / "README.md").stat().st_size > 100

    def test_readme_has_h1(self):
        content = (ROOT / "README.md").read_text(encoding="utf-8")
        assert content.startswith("#") or "\n#" in content

    def test_license_exists(self):
        assert (ROOT / "LICENSE").exists()

    def test_license_is_mit(self):
        content = (ROOT / "LICENSE").read_text(encoding="utf-8")
        assert "MIT License" in content
        assert "Shannon Brian Kelly" in content


class TestPhasePack:
    PHASE = ROOT / "7_Layer_Architecture_Phase_Blank_Template_Pack"

    def test_phase_pack_exists(self):
        assert self.PHASE.exists() and self.PHASE.is_dir()

    def test_phase_has_10_template_dirs(self):
        # 00 INDEX through 09 QA RELEASE checklist
        dirs = sorted(d.name for d in self.PHASE.iterdir() if d.is_dir())
        # Allow flexibility for additional subfolders but expect at least the core 10
        numbered = [d for d in dirs if d[:2].isdigit()]
        assert len(numbered) >= 10, f"expected at least 10 numbered template dirs; got {len(numbered)}"

    def test_phase_index_present(self):
        candidates = list(self.PHASE.glob("00_*"))
        assert candidates, "00_TEMPLATE_PACK_INDEX or similar missing"


class TestA2aMcpPack:
    A2A = ROOT / "7_Layer_A2A_MCP_Blank_Template_Pack"

    def test_a2a_pack_exists(self):
        assert self.A2A.exists() and self.A2A.is_dir()

    def test_a2a_has_at_least_6_template_dirs(self):
        dirs = sorted(d.name for d in self.A2A.iterdir() if d.is_dir())
        numbered = [d for d in dirs if d[:2].isdigit()]
        assert len(numbered) >= 6, f"expected at least 6 numbered template dirs; got {len(numbered)}"


class TestRepoCleanliness:
    def test_no_pycache_in_root(self):
        assert not (ROOT / "__pycache__").exists()

    def test_no_ds_store(self):
        assert not (ROOT / ".DS_Store").exists()

    def test_no_stray_pyc_files(self):
        # Allow .pyc inside tests/__pycache__/ (pytest's own bytecode cache)
        pycs = [p for p in ROOT.rglob("*.pyc") if "__pycache__" not in str(p)]
        assert not pycs, f"found stray .pyc files outside __pycache__: {pycs}"
