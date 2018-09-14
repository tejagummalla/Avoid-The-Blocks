import cx_Freeze
from cx_Freeze import setup

executables = [cx_Freeze.Executable("AvoidTheBlock.py")]

setup(name = "Avoid The Blocks", options = {"build_exe" : {"packages" : ["pygame"],"include_files": ["race toy.png"]}},
	executables = executables)