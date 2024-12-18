# Makefile for converting Python scripts in the "public" folder to exe using PyInstaller

# Directory containing Python scripts
SRC_DIR := src

# Directory to store the generated exe files
BUILD_DIR := bin

# PyInstaller command with the --onefile option
PYINSTALLER := pyinstaller

# List of Python scripts (excluding extension) in the "public" folder
SCRIPTS := $(patsubst $(SRC_DIR)/%.py,%,$(wildcard $(SRC_DIR)/*.py))

# Target: build all Python scripts in the "public" folder
all: build

# Target: build Python scripts in the "public" folder
build: $(addsuffix -exe, $(SCRIPTS))

# Rule to build each Python script
%-exe:
	@echo "Building exe for $*..."
	@$(PYINSTALLER) --onefile --distpath=$(BUILD_DIR) $(SRC_DIR)/$*.py
	@echo "Exe file for $* has been generated in the $(BUILD_DIR) folder."

# Target: clean generated files
clean:
	@echo "Cleaning up..."
	@rm -rf $(BUILD_DIR)
	@echo "Cleanup complete."

# Target: help - display available make targets
help:
	@echo "Available make targets:"
	@echo "  - all: Build all Python scripts in the 'public' folder."
	@echo "  - build: Build Python scripts in the 'public' folder."
	@echo "  - clean: Clean up generated files."
	@echo "  - help: Display this help message."

# Makefile phony targets
.PHONY: all build clean help
