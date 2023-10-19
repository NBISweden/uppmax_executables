# UPPMAX executables

These scripts are used to find all shared libraries that are present on Rackham but not on Dardel. The aim is then to copy all the shared library files from Rackham, place them all in a folder on Dardel and point LD_LIBRARY_PATH there and hope for the best.

# Generate lists at Dardel and Rackham

First we need to make a list of all libs that are missing at Dardel. Do that by running

```bash
# on dardel
python3 ldd_crawler.py -i /cfs/klemming/projects/snic/naiss2023-22-1027/dahlo/testarea/module_transfer/sw/bioinfo -o dardel.bioinfo.v2.out

# on rackham
python ldd_crawler.py -i /sw/bioinfo/ -o uppmax.bioinfo.out
```

Copy the lists so that you have both in the same location so you can make a diff between them.

```bash
# on dardel
rsync -aP user@rackham.uppmax.uu.se:/home/user/uppmax.bioinfo.out .
```

Then we can run the diff script on them and find the paths on Rackham for the libs that are missing on Dardel.

```bash
# on dardel
python3 ldd_diff.py -d dardel.bioinfo.out -u uppmax.bioinfo.out > bioinfo.ldd_diff.out
```

The output file `bioinfo.ldd_diff.out` contains a list of all the libraries that are missing on Dardel and their path on Rackham, one path per row.

(uglyness ahead)

We then use rsync to copy all the files listed in the file to Dardel:

```bash
mkdir libs
rsync -LaP --files-from=bioinfo.ldd_diff.out user@rackham.uppmax.uu.se:/ libs/
```

The files are saved in `libs/` but they are still structured in a file tree as they are on Rackham. To squash the file tree and get all the files in the same folder:

```bash
mkdir ld_mix
find libs/ -type f -exec cp {} ld_mix \;
```

We then include this monstrosity in our `LD_LIBRARY_PATH` and pray it will work to actually run the modules.

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cfs/klemming/projects/snic/naiss2023-22-1027/dahlo/testarea/uppmax_executables/ld_mix
```







