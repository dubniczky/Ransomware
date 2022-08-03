py := python3

# Restore demo to original version
.PHONY: restore
restore:
	@rm -rf demo
	@mkdir -p demo
	@echo "aaa" > demo/a.txt
	@echo "bbbbbb" > demo/b.txt
	@mkdir -p demo/subf
	@echo "ccccccccc" > demo/subf/c.txt

# Encrypt all files in demo
.PHONY: encrypt
encrypt:
	$(py) encrypt.py

# Generate a new asymmetric key pair for key encryption
.PHONY: generate
generate:
	$(py) generate.py
