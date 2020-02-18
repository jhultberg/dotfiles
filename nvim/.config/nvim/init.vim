" Set nvim language to english
"language en_US
" Include normal .vimrc when running neovim
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc
