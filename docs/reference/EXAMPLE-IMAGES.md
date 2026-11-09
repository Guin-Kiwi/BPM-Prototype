# BRACOL upload examples

Three author-hosted detached-leaf JPEG examples are in the ignored
`data/example-images/` folder for manual upload through the local intake form.
Choose any file with the file picker; filenames are neutral and carry no diagnosis
label. They demonstrate upload handling and may be used for a controlled-condition
comparison. Their plain backgrounds do not resemble on-plant farmer field reports;
they are not a representative sample, diagnostic evaluation set, or evidence of
realistic farmer-image performance. The [open-data plan](OPEN-DATA.md) is the single
authority for dataset selection and the next inspection step.

## Source and licence

BRACOL version 1, DOI [10.17632/yy2k5y8mxg.1](https://data.mendeley.com/datasets/yy2k5y8mxg/1),
by Renato A. Krohling, Guilherme J. M. Esgario and José A. Ventura, is licensed
CC BY 4.0. Its dataset page describes 1,747 complete Arabica leaf images and
links the source paper [arXiv:1907.11561](https://arxiv.org/abs/1907.11561).
The primary authors' [lara2018 repository](https://github.com/esgario/lara2018)
provides individually downloadable images and its classification CSV. The files
below were retrieved on 2026-11-09 from that repository's `master` raw URLs;
they were not extracted from the Mendeley archive. Attribution: Krohling, Esgario
& Ventura, “BRACOL,” version 1 (2019), CC BY 4.0; source image IDs and URLs below.

## Files and provenance

The original sample ID is the numeric filename in `classification/dataset/leaf/`.
Label fields are copied as raw codes from the authors' `classification/dataset/dataset-full.csv`
(`predominant_stress`, `severity`); codes are retained verbatim rather than
reinterpreted here. `miner`, `rust`, `phoma`, and `cercospora` are the CSV's
additional indicator fields.

| Local file | Original ID | Source URL | CSV label codes (`predominant_stress`, `severity`) | SHA-256 |
| --- | ---: | --- | --- | --- |
| `data/example-images/sample-01.jpg` | 1 | [raw JPEG](https://raw.githubusercontent.com/esgario/lara2018/master/classification/dataset/leaf/1.jpg) | `0`, `0` (all four indicators `0`) | `08e57bfe7b45a94df82df3752bcd5ee121be056db93cd63b8cce709e0ea64f15` |
| `data/example-images/sample-02.jpg` | 21 | [raw JPEG](https://raw.githubusercontent.com/esgario/lara2018/master/classification/dataset/leaf/21.jpg) | `1`, `3` (`miner=1`; others `0`) | `3f87360cb97ce622d2e1e5c64ab96b5b4febee02242d0b93c1cf629d984eb99c` |
| `data/example-images/sample-03.jpg` | 90 | [raw JPEG](https://raw.githubusercontent.com/esgario/lara2018/master/classification/dataset/leaf/90.jpg) | `2`, `4` (`rust=1`, `cercospora=1`; others `0`) | `be403cf450a1a970c9c1a4e393f7d8d56f83b8c36039c5079a76892af03138e2` |

Each downloaded example is 512×256 pixels and under 18 KB.
Local transformations: none; downloaded bytes retain the JPEG format and source image
content. On inspection, each is a complete leaf on a light background. Use the
neutral local filenames for upload; keep this source manifest separate from any
diagnosis input.
