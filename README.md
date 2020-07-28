## r2 zb stats

This repo is just meant to show some statistics on the merits of the zb command
in r2. 

### Method
The simple `main.c` is compiled twice:
1. `gcc -o static --static main.c`
2. `gcc -o normal main.c`

The `ldd` program is used on `normal` to find the libc version. That version
was copied into this repository as `libc.so.6`. Signatures were generated from
the libc file using the command `rasign2 -o libc.sdb libc.so.6`.

The `r2pipit.py` script was used to generate the below statistics. The output
of the program can be seen in `stats`. The `r2pipit.py` script attempts to run
`zb 20` on every function in `static` that starts with "sym.". The result is
parsed and basic statistics are done to see if the known correct result is in
the output.

### results

```
26.00% chance signature would be found without zb
53.62% chance correct signature is number 1 result of zb
57.63% chance correct signature is in top 5 results
58.13% chance correct signature is in top 10 results
58.50% chance correct signature is in top 15 results
58.50% chance correct signature is in top 20 results
```

Note: 26.00% is low b/c it is testing for a 100% match on graph AND byte
signatures. Where a `z.` will really only look for a 100% match on graph OR
byte signatures.

See the `stats` file for more details. Also, keep in mind this is just some
stuff I threw together so the stats might be a bit off. 

## results `e zign.graph = false`

Results are more favorable without the graph signature.

```
31.13% chance signature would be found without zb
45.75% chance correct signature is number 1 result of zb
48.38% chance correct signature is in top 5 results
48.50% chance correct signature is in top 10 results
48.75% chance correct signature is in top 15 results
48.88% chance correct signature is in top 20 results
```

So the previous `26.00%` should really be at least `31.13%`. However, `zb`
seems to benifit from using both pieces of information.
