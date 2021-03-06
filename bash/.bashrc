if [ $(uname) == "Linux" ]; then
	# Make commands colorful by default
	alias ls="ls --color=auto"
	alias grep="grep --color=auto"

	# Add auto-complete support
	if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
	    . /etc/bash_completion
	fi
elif [ $(uname) == "Darwin" ]; then
	# Add default linux style colors to macOS
	export CLICOLOR="1"
	export LSCOLORS="ExGxBxDxCxEgEdxbxgxcxd"

    alias ll="ls -l"

	# Ensure Homebrew is installed ([] must not be used in if)
	if hash brew 2>/dev/null; then
		# Add auto-complete support
		if [ -f $(brew --prefix)/etc/bash_completion ]; then
			. $(brew --prefix)/etc/bash_completion
		fi
	fi
fi

# Add ~/.local/bin to patch since it is a common installation location
PATH="$PATH:$HOME/.local/bin"

# Run all custom bash commands by default
if [ -d "$HOME/.bashrc.d" ]; then
	for i in $HOME/.bashrc.d/*; do
		if [ -r "$i" ]; then
			source "$i"
		fi
	done
	unset i
fi
