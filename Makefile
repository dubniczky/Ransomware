# Restore demo to original version
.PHONY: restore
restore:
	@rm -rf demo
	@mkdir -p demo
	@echo "aaa" > demo/a.txt
	@echo "bbbbbb" > demo/b.txt
	@mkdir -p demo/subf
	@echo "ccccccccc" > demo/subf/c.txt