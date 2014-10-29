#!/bin/sh

SRC="./src"

cp ${SRC}/bashrc ${HOME}/.bashrc
cp ${SRC}/tmux ${HOME}/.tmux.conf
cp ${SRC}/vimrc ${HOME}/.vimrc

mkdir -p ${HOME}/.config/fontconfig
cp fonts.conf ${HOME}/.config/fontconfig/
