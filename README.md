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
total : 921
```
There were 921 functions processed total.

```
zb useless : 261
```
Of those, 261 resulted in a correct perfect match on bytes and graph
signatures. This means `zb` was of no real help, since normal matching
succeded. So 28.33% success. Of the 261 perfect results, 59 of them had perfect
false positives.

```
total not perfect : 660
```
So there were 660 functions left where the signature did not match perfectly.

```
zb best : 125
```
Of the 660 not perfect cases `zb` returned the correct signature as the top
result. This signature was not a perfect match, but it was the closest match.
This means, with the 261 perfect matches above, `zb` raises the 28.33% match
percentage to 41.91% with just one result.

```
in top 5 : 197
in top 10 : 221
in top 15 : 235
in top 20 : 246
```
These numbers show when `zb` produced the correct result in the top `n`
results. So `zb` was able to find the correct signature in the top 5 results
197 times. Raising 51.91% to 52.33%.

### False Positives
I am not foccussed on dealing with these yet. This is included for
completeness.

```
perfect fp : 111
```
111 times there was a perfect match between a function and at least one wrong
signature.

```
perfect with fp : 59
```
59 times there were perfect matches for the correct signature and at least one
wrong signature.

# why false positives

Like I said, I am not focused on this but a quick peek will help. But a quick
peek already found a bunch:

```
sym._nl_load_domain.cold
1.00000  1.00000 B  1.00000 G   sym.strfromf128.cold
1.00000  1.00000 B  1.00000 G   sym.__GI___printf_fp_l.cold
1.00000  1.00000 B  1.00000 G   sym.strfroml.cold
1.00000  1.00000 B  1.00000 G   sym.round_away.cold
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold
1.00000  1.00000 B  1.00000 G   sym.getifaddrs_internal.cold
1.00000  1.00000 B  1.00000 G   sym.__regerror.cold
1.00000  1.00000 B  1.00000 G   sym._nl_load_domain.cold
1.00000  1.00000 B  1.00000 G   sym.strfromd.cold
1.00000  1.00000 B  1.00000 G   sym._IO_seekoff_unlocked.cold
1.00000  1.00000 B  1.00000 G   sym.re_compile_internal.cold
1.00000  1.00000 B  1.00000 G   sym.__printf_fphex.cold
1.00000  1.00000 B  1.00000 G   sym.__GI_authunix_create.cold
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_5
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_4
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_7
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_6
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_1
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_3
1.00000  1.00000 B  1.00000 G   sym.round_and_return.cold_2
```

This also means there was a 100% match on `sym.strfromf128.cold` for all of the
above. So this alone accounts for at least 20 of the 59 `perfect with fp`.

The `sym._nl_load_domain.cold` function looks like: 
```
[0x00025727]> pdf
┌ 5: sym._nl_load_domain.cold ();
│ bp: 0 (vars 0, args 0)
│ sp: 0 (vars 0, args 0)
│ rg: 0 (vars 0, args 0)
└           0x00025727      e800000000     call sym.abort              ; void abort(void)
```

So apparently the default `zign.minsz` of 16 is not properly enforced. I will
work on fixing this bug very soon.
