" compile and run commands
"nnoremap <f3> :wa<cr>:silent! cexpr system("msbuild build\\Brillo-Engine.sln /nologo /v:m")<cr>:copen<cr>
"nnoremap <S-f3> :wa<cr>:silent! cexpr system("make -C build clean & make -C build")<cr>:copen<cr>G
"nnoremap <f4> :call RunProgram("bin\\tools\\Debug\\tools engine")<cr>
"nnoremap <f4> :call RunProgram("bin\\tools\\Debug\\tools engine projects/testbed")<cr>
nnoremap <f4> :call RunProgram("python main.py")<cr>
nnoremap <f2> :wa<cr>:!premake\\premake5.exe vs2019<cr>
"nnoremap <f2> :wa<cr>:!premake\\premake5.exe vs2019<cr>:!premake\\premake5.exe export-compile-commands<cr>

"nnoremap <f8> :!devenv .<cr><cr>
nnoremap <f8> :!explorer .<cr><cr>

let g:run_program_split_vertical=1

" Error format for MSVC
set errorformat=\ %#%f(%l\\\,%c):\ %m

let g:ctrlp_custom_ignore = {
  \ 'dir':  '\v[\/]\.(git|hg|svn)|target|build|Build|bin|docs$',
  \ 'file': '\v\.(exe|so|dll|pdb)$',
  \ 'link': 'some_bad_symbolic_links',
  \ }
