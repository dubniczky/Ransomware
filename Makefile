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
	$(py) encrypt.py keys/public.key

# Generate a new asymmetric key pair for key encryption
.PHONY: generate
generate:
	$(py) generate.py

# Unlock encryption key
.PHONY: unlock
unlock:
	@$(py) unlock.py keys/private.key $(shell cat secret.key)

# Decrypt file
.PHONY: decrypt
decrypt:
	@$(py) decrypt.py map.log $(shell make unlock)


# Linting
.PHONY: lint
lint:
	@$(py) -m prospector ./

# Installing packages
.PHONY: install
install:
	@pip install -r requirements.txt