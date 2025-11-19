Create a new command `wm` which stands for working memory
it assumes a environment variable with `wm` exist.


`tos wm` would print the working memory location
`tos wm project1` will create a folder 'project1' under the location mentioned in wm.
this also open the the project1 in vs code. by default it apply the default template 

in addition user can give specific template name
`tos wm project1 -t template1 template2` this apply the template template1 and template2
similar to `tos init -t template1` and `tos init -t template2` from the `project1`

If `project1` exist, it simply move to that folder and open in vs code by 'code '

Also introduce `t wm --recent` which will look at the history log and filter only those having `wm` command


Need to correct the `t wm --recent` function.

`t wm --recent` or `t wm --recent 0` should look at the which will look at the history log of wm command and find the project used and open that project.
for example if user called `t wm ak1` first and `t wm ak2`
the when he enters `t wm --recent` it should should treat the command as `t wm ak2`
if user enter `t wm --recent 1`, then it should switch to second last and so on. so it goes to `t wm ak1` 