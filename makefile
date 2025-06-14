.PHONY: run clean

# Run this and will launch a local server that hosts the website.
# We will connect with firefox to it.
run: gemset.nix
	(sleep 4s ; firefox "localhost:4000") &
	nix-shell -p bundler -p jupyter --run "bundle exec jekyll serve"

clean:
#	Run this when some dependencies broke.
#	rm -rf ~/.local/share/gem/ruby/3.3.0
	rm -f gemset.nix

gemset.nix:
	nix-shell -p bundler -p bundix --run 'bundler update; bundler lock; bundler package --no-install --path vendor; bundix -l; rm -rf vendor .bundle'

# This generates the _bibliography/papers.bib file that is used as source for the website's bibliographical data.
generate-papers:
	nix-shell -p python3Packages.bibtexparser --run \
	  "python _bibliography/generate.py \
	     BibPax/papers.bib \
	     BibTags \
	     _bibliography/papers.bib"
