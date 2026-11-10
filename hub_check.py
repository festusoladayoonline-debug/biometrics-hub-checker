"""BioMetrics & HealthData Hub - course checker.

Gives you feedback on your exercises (a tick or a cross, plus a hint) and counts your progress.
You do not need to read or change this file. Answers are stored as one-way fingerprints (hashes), never as
readable answers. This is feedback only: your instructor's marking is separate.
"""
import hashlib
import json
import math
import numbers

try:
    from IPython import get_ipython
except Exception:                                   # pragma: no cover
    get_ipython = None

_SALT = "bmhh-v1"
SPEC = json.loads("{\"items\":{\"K1.1\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_1\",\"h\":\"22e1e23c0f862c7c94bb\"}]},\"1.2\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"bmi_2\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"a70e72afbe0d272000c2\",\"f0dd737bbc2607cecc1b\",\"d4f9a4b77d89076b8393\"]}],\"hint\":\"Copy the line from the example above and use the new variable name.\"},\"1.3\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"mean_hr\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"cabbccd1b6cdbbc12825\",\"c4ecf0d21d6b962cae37\",\"6f59b49de69562de8b04\"]}],\"hint\":\"Without brackets, only `hr_3` would be divided by 3.\"},\"K1.2\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_2\",\"h\":\"4b08fe13727678089e1f\"}]},\"K1.3\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_3\",\"h\":\"efa6a9d156b503cbbf0b\"}]},\"Q1.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_1\",\"min_words\":25}]},\"1.4\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"id_upper\",\"t\":\"str\",\"h\":[\"c3d3b3eef980c9f9729b\"]},{\"kind\":\"scalar\",\"var\":\"id_length\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8bc26da3a499f7cc8067\",\"73ba998ed13cd73a6a17\",\"a8c0ce4f587267652309\"]}],\"hint\":\"Methods have brackets even when they are empty: `.upper()`.\"},\"1.5\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"summary\",\"t\":\"str\",\"h\":[\"c124fd9dcf10f80250c2\"]}],\"hint\":\"Start with `f\\\"Patient aged {age} with ...`.\"},\"K1.4\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_4\",\"h\":\"9902bdf23510290948cc\"}]},\"1.6\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"oldest\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8126a7e112619870d8af\",\"6f8221a09f6c091d6b4c\",\"98efc6afe533b75bbad2\"]},{\"kind\":\"scalar\",\"var\":\"n_patients\",\"t\":\"num\",\"w\":0.5,\"h\":[\"f040d8b21135f33d3908\",\"ffb3763c74b663ed4841\",\"e02ecbc4cf00c28c7f37\"]},{\"kind\":\"scalar\",\"var\":\"mean_age\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"2b80c18af254100439cb\",\"03e6e1229c979d08e3e3\",\"97da97cf8eadbaadb745\"]}]},\"1.7\":{\"items\":[{\"kind\":\"list_eq\",\"var\":\"middle\",\"h\":\"79ac89cbf7faebc49f54\"}],\"hint\":\"The stop number is not included, so use 3.\"},\"K1.5\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_5\",\"h\":\"e4c0b4c7f577029871c0\"}]},\"1.8\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"patient_sex\",\"t\":\"str\",\"h\":[\"22211055219956da5287\"]},{\"kind\":\"scalar\",\"var\":\"n_entries\",\"t\":\"num\",\"w\":0.5,\"h\":[\"f040d8b21135f33d3908\",\"ffb3763c74b663ed4841\",\"e02ecbc4cf00c28c7f37\"]}]},\"K1.6\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_6\",\"h\":\"7663b39854757d9511e3\"}]},\"1.9\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"status\",\"t\":\"str\",\"h\":[\"443b143b560c18075f28\"]}],\"hint\":\"Remember the colons and the four spaces of indentation.\"},\"K1.7\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_7\",\"h\":\"c1f870635cf93725a94b\"}]},\"1.10\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"n_high\",\"t\":\"num\",\"w\":0.5,\"h\":[\"c9d0a1d6275465c24963\",\"8d0160ded45c173a951d\",\"21a132abc07c856a2de3\"]}],\"hint\":\"Copy the 'count with a condition' example and change the list and the number.\"},\"1.11\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"total_hr\",\"t\":\"num\",\"w\":0.5,\"h\":[\"44adcdc365ba021a2096\",\"43c43fdc4c5a83fb438b\",\"5c77f5c78670e7c71a6c\"]}]},\"K1.8\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_8\",\"h\":\"ea7be4b5f88670755c98\"}]},\"Q1.2\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_2\",\"min_words\":25}]},\"1.12\":{\"items\":[{\"kind\":\"func\",\"var\":\"to_fahrenheit\",\"w\":1e-06,\"tests\":[[[37],{\"t\":\"num\",\"h\":[\"e6eab6bf4adae9cf4adb\",\"857dc86673dc1fec4056\",\"e9d5a083892f96bce839\"]}],[[0],{\"t\":\"num\",\"h\":[\"2ce7093e8b5ab9dab40a\",\"5461e7f29537df29e75a\",\"b227e1d4dd7d639b4ab5\"]}],[[100],{\"t\":\"num\",\"h\":[\"455a3083ec05110e41bb\",\"2c1c231f8f710f15a0c5\",\"0fcc45e97f702c5f8b5d\"]}],[[-40],{\"t\":\"num\",\"h\":[\"b35f396f80e8d2cb841c\",\"026c6a56604b1e0ee9e7\",\"7dca49faa1e3c5af931c\"]}]]}],\"hint\":\"`return` hands the answer back; `print` only shows it.\"},\"1.13\":{\"items\":[{\"kind\":\"func\",\"var\":\"bmi_category\",\"w\":1e-09,\"tests\":[[[18.5],{\"t\":\"str\",\"h\":[\"61bff18ab01c54955bf0\"]}],[[24.99],{\"t\":\"str\",\"h\":[\"61bff18ab01c54955bf0\"]}],[[25],{\"t\":\"str\",\"h\":[\"5a9e998f6656dc99ecc3\"]}],[[29.99],{\"t\":\"str\",\"h\":[\"5a9e998f6656dc99ecc3\"]}],[[30],{\"t\":\"str\",\"h\":[\"7dd1a8514bfc14b9a80a\"]}],[[15],{\"t\":\"str\",\"h\":[\"d6c85ad4c476cd03e1d5\"]}]]}],\"hint\":\"Test the smallest cut-off first. Exactly 25 belongs to the higher group.\"},\"K1.9\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_9\",\"h\":\"091e10e3c5ee05416b5e\"}]},\"Q1.3\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_3\",\"min_words\":25}]},\"K1.10\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_10\",\"h\":\"3854a190b5e5e5ac00fd\"}]},\"1.14\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"n_rows\",\"t\":\"num\",\"w\":0.5,\"h\":[\"a04ceee8477608b415c5\",\"5577e49050cf7620fb70\",\"2629a4d5378aa6d4979e\"]},{\"kind\":\"scalar\",\"var\":\"n_cols\",\"t\":\"num\",\"w\":0.5,\"h\":[\"02e715c503abed57b368\",\"560efdcfab0c7523bf4e\",\"6310fab24b2ac813094b\"]}]},\"Q1.4\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_4\",\"min_words\":25}]},\"1.15\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"oldest_age\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8126a7e112619870d8af\",\"6f8221a09f6c091d6b4c\",\"98efc6afe533b75bbad2\"]},{\"kind\":\"scalar\",\"var\":\"youngest_age\",\"t\":\"num\",\"w\":0.5,\"h\":[\"0c10a8660fa8164e9db4\",\"813d8d2c5a6d255eb68e\",\"154a51f7dd6bae8ba53a\"]},{\"kind\":\"columns\",\"var\":\"small\",\"h\":\"b96a4700679ad36e5d35\"}],\"hint\":\"Two pairs of square brackets when you want several columns.\"},\"K1.11\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_11\",\"h\":\"1f68176e9fe437757f8b\"}]},\"1.16\":{\"items\":[{\"kind\":\"rows\",\"var\":\"smokers\",\"w\":0.5,\"h\":[\"fe8128cfbb5fb692a025\",\"b6f33d7b7c92b744944f\",\"844b16dae60d8753399f\"]}],\"hint\":\"`==` compares; a single `=` would store.\"},\"1.17\":{\"items\":[{\"kind\":\"rows\",\"var\":\"older_women\",\"w\":0.5,\"h\":[\"6623e72113e4cb419212\",\"24ee86d37b5604cf6017\",\"2496a6fdf51e15087313\"]}],\"hint\":\"Two conditions, each in brackets, joined by `&`.\"},\"K1.12\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_12\",\"h\":\"e7d28fd4c967314ceddc\"}]},\"1.18\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"median_sysbp\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"627f4f8f94d972e29dcc\",\"bd0d6f17acf6c2b74e55\",\"9d57660d96f53e82479c\"]},{\"kind\":\"scalar\",\"var\":\"mean_bmi\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"f7680bf0baa3d46d8c2b\",\"ffadcebb17545c4b37d8\",\"87099809fc041e5fc43e\"]}]},\"1.19\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"chd_rate\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"2098f30f796b8dbe8620\",\"dc75fae576f1b6666a66\",\"fd0ad4cf275e59047608\"]}]},\"Q1.5\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_5\",\"min_words\":25}]},\"K1.13\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_13\",\"h\":\"d77e7fbf18e04964ddf3\"}]},\"1.20\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"n_missing_glucose\",\"t\":\"num\",\"w\":0.5,\"h\":[\"73d379d4efc1220da173\",\"df6fc1c2e3dbeef9b578\",\"05ceba6462b01cf5563d\"]},{\"kind\":\"scalar\",\"var\":\"pct_missing_glucose\",\"t\":\"num\",\"w\":0.01,\"h\":[\"2b907513b19bbca246f4\",\"77c1c4c433e892a4b505\",\"576fa84c58250ba1dded\"]},{\"kind\":\"scalar\",\"var\":\"most_missing_col\",\"t\":\"str\",\"h\":[\"8faafa61bb9194195976\"]}]},\"Q1.6\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_6\",\"min_words\":25}]},\"K1.14\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_14\",\"h\":\"29a7cdf2d16cb9a984e4\"}]},\"1.21\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"n_hr_flag\",\"t\":\"num\",\"w\":0.5,\"h\":[\"b7a85a1c50655d570edd\",\"fac80b4cc4a1055efef3\",\"27d7221ca8b33c2cc459\"]}]},\"K1.15\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_15\",\"h\":\"6e89f8952d9e85e00f1f\"}]},\"1.22\":{\"items\":[{\"kind\":\"series_close\",\"var\":\"chd_by_smoker\",\"w\":1e-06,\"i\":\"c9d96b9715bc346885e7\",\"s\":[[\"86f09dcf2c2f21466b16\",\"a0acb0c3e65091cf75f7\",\"6dbd614d1a4c637c30e5\"],[\"62de1cd9ced907502df0\",\"99484c59655c3a881ceb\",\"a3304ea9f349f3bf286b\"]]}]},\"1.23\":{\"items\":[{\"kind\":\"series_close\",\"var\":\"age_by_chd\",\"w\":1e-06,\"i\":\"c9d96b9715bc346885e7\",\"s\":[[\"affd08dc24ac6b1b0647\",\"05aa1c8f3a25c55d5fce\",\"1bcba3ca3b993def2e44\"],[\"e9f9fa58f0b2e413f111\",\"bdc07a299ccbe8efb8d1\",\"2070a0f974e6ef19977d\"]]}]},\"Q1.7\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_7\",\"min_words\":25}]},\"K1.16\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_16\",\"h\":\"bbb9d2ea50beeecbc81f\"}]},\"1.24\":{\"items\":[{\"kind\":\"source_has\",\"var\":null,\"words\":[\"hist\",\"title\",\"xlabel\",\"ylabel\"]}],\"hint\":\"Copy the BMI example and change the column and the labels.\"},\"1.25\":{\"items\":[{\"kind\":\"source_has\",\"var\":null,\"words\":[\"bar\",\"title\",\"xlabel\",\"ylabel\"]}]},\"Q1.8\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_1_8\",\"min_words\":25}]},\"K1.17\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_1_17\",\"h\":\"69bd44a4d7b4304e0b72\"}]},\"R1.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"research_1_1_summary\",\"min_words\":40}]},\"2.1\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"hr_median\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"dcbf3786d427ac3d1d78\",\"e7378fdb8f866abf5968\",\"94cd6729c34ce6974f65\"]},{\"kind\":\"source_has\",\"var\":null,\"words\":[\"hist\",\"axvline\",\"title\",\"xlabel\",\"ylabel\"]}],\"hint\":\"Copy the glucose example and change the column name.\"},\"2.2\":{\"items\":[{\"kind\":\"series_close\",\"var\":\"edu_props\",\"w\":1e-06,\"i\":\"5383ef1d11c8e9c7a6be\",\"s\":[[\"439e3775841b49edf4d3\",\"b60b1997433d4c7f3f00\",\"4889249ab86cf5605ba6\"],[\"84d7d85e5d6c1f9d67ae\",\"c28b704263663edf0d84\",\"c265d67b5a69c6f79bcf\"],[\"537b96b8d2128e6f45de\",\"7f448f10f91786b95b57\",\"7fea361aa8bbea413a8e\"],[\"3a5066858e1696c5717e\",\"ab733f1f3968626f56f2\",\"7f570a66cd97f0f468de\"]]}]},\"Q2.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_1\",\"min_words\":25}]},\"K2.1\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_1\",\"h\":\"a91ef3d39e91ec1abe13\"}]},\"2.3\":{\"items\":[{\"kind\":\"series_close\",\"var\":\"median_sbp_by_sex\",\"w\":1e-06,\"i\":\"c9d96b9715bc346885e7\",\"s\":[[\"fc4864a65b6904bbb16f\",\"27685b85b93b4e34da19\",\"9d1844e2d87568781ba8\"],[\"fc4864a65b6904bbb16f\",\"27685b85b93b4e34da19\",\"9d1844e2d87568781ba8\"]]},{\"kind\":\"source_has\",\"var\":null,\"words\":[\"violinplot\",\"title\",\"xlabel\",\"ylabel\"]}]},\"2.4\":{\"items\":[{\"kind\":\"source_has\",\"var\":null,\"words\":[\"scatter\",\"alpha\",\"title\",\"xlabel\",\"ylabel\"]}]},\"Q2.2\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_2\",\"min_words\":25}]},\"K2.2\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_2\",\"h\":\"3c5e4f2522d0af14cb8e\"}]},\"2.5\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"r_age_dia\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"b27c6bf50380c27c142c\",\"ec81b6ba1b7bfdbf25bf\",\"edd3ad55c7ca479aa530\"]},{\"kind\":\"scalar\",\"var\":\"rho_age_sysbp\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"f8f9e4eba706616de5f4\",\"7161349158db6fe7c68f\",\"01b2a23db71675e8b403\"]}]},\"2.6\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"strongest_with_sysbp\",\"t\":\"str\",\"h\":[\"1dee539988562fa9973f\"]}]},\"Q2.3\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_3\",\"min_words\":25}]},\"K2.3\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_3\",\"h\":\"1ae980735d42b6de395b\"}]},\"2.7\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"welch_p\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"fa567cbb97f07e4569a8\",\"f4626b0548a8c8ff62d3\",\"69625a8de0be7452e260\"]},{\"kind\":\"scalar\",\"var\":\"d_smoking\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"556e97746dcb414dffe2\",\"cebbf4163ad38d45fb2a\",\"85a4f6ea53799c5fe94f\"]}]},\"2.8\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"smoking_diff\",\"t\":\"num\",\"w\":0.001,\"h\":[\"82660b6599cb11c19573\",\"a7e3132e9b72d445e1bb\",\"7a2dc1747524fc08da54\"]},{\"kind\":\"scalar\",\"var\":\"ci_low\",\"t\":\"num\",\"w\":0.05,\"h\":[\"6e3a37d0394fcdc79b0a\",\"3d7df263d55975f69474\",\"bbaa27a5a7017b7b2fa9\"]},{\"kind\":\"scalar\",\"var\":\"ci_high\",\"t\":\"num\",\"w\":0.05,\"h\":[\"d78a3ab8a265b794ef68\",\"6d9bc2c7faa0ba47b622\",\"fa7578e806efc0e473c3\"]}]},\"2.9\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"mwu_p\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"fa567cbb97f07e4569a8\",\"f4626b0548a8c8ff62d3\",\"69625a8de0be7452e260\"]},{\"kind\":\"scalar\",\"var\":\"cles\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"1f9b7b6050a463449e18\",\"0cfafe0b729744c028a9\",\"585b17b122cf4f4eb35b\"]}]},\"Q2.4\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_4\",\"min_words\":25}]},\"K2.4\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_4\",\"h\":\"38a428a505dc82530a1c\"}]},\"2.10\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"chi2_sex_p\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"e8780944278784a6f46c\",\"a0a1aca0b15a067c5168\",\"516530376c26a44b1b26\"]},{\"kind\":\"scalar\",\"var\":\"v_sex\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"c1bf03da7a83e8b6a5e8\",\"7371777d5753d4ce0f9e\",\"9d79fec9bea5225429f1\"]},{\"kind\":\"scalar\",\"var\":\"or_sex\",\"t\":\"num\",\"w\":0.001,\"h\":[\"d6da6fd1026f6f957f3f\",\"15ac6f38442117dd0c34\",\"9e5ce1cdd3ff5eea48d8\"]}]},\"2.11\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"min_expected_count\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"e5afe5a1791d5e68faea\",\"1f3f5c1bfe4823c4fbc4\",\"bd88684e9bab05eb21dd\"]},{\"kind\":\"scalar\",\"var\":\"or_diabetes\",\"t\":\"num\",\"w\":0.001,\"h\":[\"3c20113d5fbf47f7f7be\",\"93892b528dcf0d50158c\",\"97499fca429093493cca\"]}]},\"Q2.5\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_5\",\"min_words\":25}]},\"K2.5\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_5\",\"h\":\"ae294155af650641c3f7\"}]},\"2.12\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"eta_sq_age_band\",\"t\":\"num\",\"w\":0.001,\"h\":[\"1407af89249a29db25c7\",\"400f539b1abfc5ced2eb\",\"b7e390deb8e53dfbb165\"]},{\"kind\":\"scalar\",\"var\":\"kruskal_p_age_band\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"fa567cbb97f07e4569a8\",\"f4626b0548a8c8ff62d3\",\"69625a8de0be7452e260\"]}]},\"Q2.6\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_6\",\"min_words\":25}]},\"K2.6\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_6\",\"h\":\"67d75d292886093649a9\"}]},\"2.13\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"r_age_dia\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"b27c6bf50380c27c142c\",\"ec81b6ba1b7bfdbf25bf\",\"edd3ad55c7ca479aa530\"]},{\"kind\":\"scalar\",\"var\":\"r_ci_low\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"f56fb7f0a058e81dff72\",\"0d63076abca828ff5473\",\"af79aa0c1723dcfc443b\"]},{\"kind\":\"scalar\",\"var\":\"r_ci_high\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"b58acb7927a7f1a8c39e\",\"b52f68c7d824a3ce82ee\",\"e350c12259122be50166\"]},{\"kind\":\"scalar\",\"var\":\"slope_dia_per_decade\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"703e38c399c7e1390af4\",\"2f78955ecaefe5423bcc\",\"7dd7213edec547c30cda\"]}]},\"Q2.7\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_7\",\"min_words\":25}]},\"2.14\":{\"items\":[{\"kind\":\"dict_close\",\"var\":\"sex_pvals\",\"w\":0.0007127792459020678,\"s\":{\"age\":[\"22ada4eea4442697a00d\",\"c21d7e3df51fe33ce1cc\",\"924f293e05317c99ee34\"],\"cigsPerDay\":[\"6d3bf2072dcbaf67a82e\",\"37779bab3c4ce15d27d1\",\"a654dbf11f29411bda14\"],\"totChol\":[\"6d3bf2072dcbaf67a82e\",\"37779bab3c4ce15d27d1\",\"a654dbf11f29411bda14\"],\"sysBP\":[\"5a293bf125a7ec735c69\",\"eeaadd3a4e33b6e7ca47\",\"5335c8734105ce19ee01\"],\"diaBP\":[\"6d3bf2072dcbaf67a82e\",\"37779bab3c4ce15d27d1\",\"a654dbf11f29411bda14\"],\"BMI\":[\"6d3bf2072dcbaf67a82e\",\"37779bab3c4ce15d27d1\",\"a654dbf11f29411bda14\"],\"heartRate\":[\"6d3bf2072dcbaf67a82e\",\"37779bab3c4ce15d27d1\",\"a654dbf11f29411bda14\"],\"glucose\":[\"661abdbc3820ddf2c00f\",\"318d48474a7c65829ace\",\"a59fde1d9451b5bfc5df\"]}},{\"kind\":\"scalar\",\"var\":\"n_sig_raw\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8bc26da3a499f7cc8067\",\"73ba998ed13cd73a6a17\",\"a8c0ce4f587267652309\"]},{\"kind\":\"scalar\",\"var\":\"n_sig_bonf\",\"t\":\"num\",\"w\":0.5,\"h\":[\"e02ecbc4cf00c28c7f37\",\"3198bb12f84ffb88a840\",\"8bc26da3a499f7cc8067\"]},{\"kind\":\"scalar\",\"var\":\"n_sig_bh\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8bc26da3a499f7cc8067\",\"73ba998ed13cd73a6a17\",\"a8c0ce4f587267652309\"]}]},\"Q2.8\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_8\",\"min_words\":25}]},\"K2.7\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_2_7\",\"h\":\"8c244bdf81fe3d24cd54\"}]},\"Q2.9\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_9\",\"min_words\":25}]},\"Q2.10\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_2_10\",\"min_words\":25}]},\"R2.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"research_2_1_summary\",\"min_words\":40}]},\"Q3.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_1\",\"min_words\":25}]},\"K3.1\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_1\",\"h\":\"349976cf6d8670638cfa\"}]},\"3.1\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"prev_train\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"7a2808b57e37fbb3f06b\",\"9bff93a2b42c6ffad972\",\"9f2de44e4c146929ed23\"]},{\"kind\":\"scalar\",\"var\":\"prev_val\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"7720f6072a1d3fb60922\",\"6ca6fee273a735f192fc\",\"dce1a94ba3293f3963d9\"]},{\"kind\":\"scalar\",\"var\":\"prev_test\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"7720f6072a1d3fb60922\",\"6ca6fee273a735f192fc\",\"dce1a94ba3293f3963d9\"]},{\"kind\":\"scalar\",\"var\":\"n_overlap\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8faa2b1b177c157175ad\",\"0ce5abada10f0db8cc8c\",\"69b5bd1f1073e0fb2527\"]}]},\"Q3.2\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_2\",\"min_words\":25}]},\"K3.2\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_2\",\"h\":\"bca516f59fe87d86984e\"}]},\"3.2\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"n_missing_glucose_train\",\"t\":\"num\",\"w\":0.5,\"h\":[\"2bda38cf968d23d6c1a4\",\"dc4648675c1aa6e2b568\",\"ad0afa9a51f1cecef196\"]},{\"kind\":\"scalar\",\"var\":\"bmi_mean_train\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"770a4e1050dd1425ff21\",\"31c667e47fae6208ad04\",\"d064d81092b3a4b56ac3\"]},{\"kind\":\"scalar\",\"var\":\"bmi_mean_all\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"f7680bf0baa3d46d8c2b\",\"ffadcebb17545c4b37d8\",\"87099809fc041e5fc43e\"]},{\"kind\":\"scalar\",\"var\":\"bmi_mean_gap\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"96d4c419465696ac50a4\",\"2acce0f9fcbcae25ae4b\",\"1f0caae802ef1975dc9e\"]}]},\"Q3.3\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_3\",\"min_words\":25}]},\"K3.3\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_3\",\"h\":\"c738054a46f171dacba0\"}]},\"3.3\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"glucose_skew_raw\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"c7b576a784edb22ba0d4\",\"26ef6c07a48c4daf3477\",\"d5a367c0e371bb9a3bda\"]},{\"kind\":\"scalar\",\"var\":\"glucose_skew_log\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"1dad88196495d72f94b6\",\"1e2be91b2a267563beb1\",\"b90c3e080e082869ed5e\"]}]},\"K3.4\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_4\",\"h\":\"3965e0aeee2906fea499\"}]},\"3.4\":{\"items\":[{\"kind\":\"series_close\",\"var\":\"vif_primary\",\"w\":0.001,\"i\":\"66c93be560519b3a0ae9\",\"s\":[[\"9310239f09dec6550e11\",\"0faf9f0532c139f1c126\",\"bf20ca7f6f56bcc5297b\"],[\"11d30b4285606f590a9d\",\"9ec1d17739885abb37c2\",\"82dd04ad059d04fb636a\"],[\"4bc16ed382afb2656f86\",\"c235856d134d5b35c805\",\"c103be31c63df3696783\"],[\"46637feb3c62ea6692fe\",\"4ca15f2e8daf1ef5dcf4\",\"c6607684d253fad18c48\"],[\"335398656f47c72d9f63\",\"6f7fa28498809693f0af\",\"842cea926d348bd6107a\"],[\"2500f83b81d2831a359b\",\"ce7ab7f47e782a3bf15e\",\"2ddff505fa18cbfe279d\"],[\"fcdfb27bffe6fd0320fd\",\"1ef7d247414f57c0d586\",\"2d8f52595df23760be42\"],[\"dc783c92debcdeef906a\",\"0f8cdca8d2fb73665d1c\",\"109848dab7cb6a8decf5\"],[\"34f8e27473cf5f91c948\",\"8f9fc28087f43209941e\",\"02c96fd81fa52dc6e273\"],[\"b7627a0836ceee7d4a09\",\"68420d13a5e9a2fcfc02\",\"3dbb128d2954ee1f6e31\"]]},{\"kind\":\"scalar\",\"var\":\"max_vif_primary\",\"t\":\"num\",\"w\":0.001,\"h\":[\"4bc16ed382afb2656f86\",\"c235856d134d5b35c805\",\"c103be31c63df3696783\"]}]},\"Q3.4\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_4\",\"min_words\":25}]},\"K3.5\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_5\",\"h\":\"df3fc34a553239d89a83\"}]},\"3.5\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"slope_age_simple\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"4d21606ce75b93165e61\",\"c4d3cb4da92082710748\",\"c269788aa68a2b42c393\"]},{\"kind\":\"scalar\",\"var\":\"r2_simple\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"adfabd82b9b0f2a737aa\",\"6648cfd947538520ad6e\",\"edac533ff23eef688c5a\"]}]},\"3.6\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"age_coef\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"f8509eca7efb975eb2d0\",\"b876617f241c12b81e4b\",\"d3fb533a15b2d3b7ff4c\"]},{\"kind\":\"scalar\",\"var\":\"age_ci_low\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"c191cee9e6f990731bb2\",\"908d9ccf7dcc6457498a\",\"2dfe38cbff318a8e7158\"]},{\"kind\":\"scalar\",\"var\":\"age_ci_high\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"1192cb39a8f8f67725b2\",\"7b544aa44c84b22af92e\",\"4ed6a19e0d484ca23ddc\"]},{\"kind\":\"scalar\",\"var\":\"adj_r2\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"5e64f9d095292f9c82af\",\"0d487200480af7723b36\",\"9a6960f17ec39a471ae0\"]}]},\"3.7\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"rmse_val\",\"t\":\"num\",\"w\":0.001,\"h\":[\"46b2170a7b1191882140\",\"b6037c0483b7dd53ad0d\",\"195ae646b9a5ba7565fb\"]},{\"kind\":\"scalar\",\"var\":\"r2_val\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"55d6bfae96a82f8de65c\",\"559947d6da4268d7e295\",\"ecf0791b63c548b77299\"]}]},\"Q3.5\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_5\",\"min_words\":25}]},\"Q3.6\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_6\",\"min_words\":25}]},\"K3.6\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_6\",\"h\":\"877f6233b8c5e6f0d7a1\"}]},\"3.8\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"resid_skew_raw\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"54aa2d949076b63b482a\",\"1a16a3bfb1e1584167e4\",\"5451c444a2ad6dc7f73e\"]},{\"kind\":\"scalar\",\"var\":\"resid_skew_log\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"1f2444715654400f6679\",\"3c5e629b7934215f3911\",\"3f672f266128e9d16807\"]},{\"kind\":\"scalar\",\"var\":\"age_pct_per_decade\",\"t\":\"num\",\"w\":0.001,\"h\":[\"f8db45165bf0c2071991\",\"26421f6b1d5ef3bfed0d\",\"0704e0c7f8ce598bc70e\"]}]},\"Q3.7\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_7\",\"min_words\":25}]},\"K3.7\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_7\",\"h\":\"8121cbb268b7d395ab7b\"}]},\"3.9\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"or_age_dec\",\"t\":\"num\",\"w\":0.001,\"h\":[\"b384afdd4112ad7345ca\",\"70e479745e034184dbc0\",\"c96581dcca1a5e9932b7\"]},{\"kind\":\"scalar\",\"var\":\"or_age_low\",\"t\":\"num\",\"w\":0.001,\"h\":[\"9136863519f2ee2a23da\",\"1698599b0aefec1dd87c\",\"571d2bdebf301ac824df\"]},{\"kind\":\"scalar\",\"var\":\"or_age_high\",\"t\":\"num\",\"w\":0.001,\"h\":[\"14eb8227b205d63f9a52\",\"a89b676dc3c7e9f9b806\",\"d15ac4419eb4b2a8b5af\"]}]},\"3.10\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"or_cigs_unadj\",\"t\":\"num\",\"w\":0.001,\"h\":[\"9617213caf8b12d21b81\",\"669766de373f12fd13f5\",\"6ccf2000c789d6c29351\"]},{\"kind\":\"scalar\",\"var\":\"or_cigs_adj\",\"t\":\"num\",\"w\":0.001,\"h\":[\"d48b0114367c134d04f8\",\"0d365f1a984bd83da6a6\",\"4131d5ba6355bfad0fac\"]}]},\"Q3.8\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_8\",\"min_words\":25}]},\"Q3.9\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_9\",\"min_words\":25}]},\"K3.8\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_8\",\"h\":\"e5710b1aee3e11882d98\"}]},\"3.11\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"delta_r2_bmi\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"7eb9bdf05a4c365513f1\",\"e92fd5d9e51d457ff52f\",\"e95101213524a8b0dfd7\"]},{\"kind\":\"scalar\",\"var\":\"delta_r2_glucose\",\"t\":\"num\",\"w\":0.0001,\"h\":[\"f50097453c5ba381e3c9\",\"38f141a4d0871b005911\",\"64da7e8d0b796303b160\"]}]},\"Q3.10\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_10\",\"min_words\":25}]},\"K3.9\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_3_9\",\"h\":\"db4568e3135cd7282691\"}]},\"Q3.11\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_11\",\"min_words\":25}]},\"Q3.12\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_3_12\",\"min_words\":25}]},\"R3.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"research_3_1_summary\",\"min_words\":40}]},\"4.1\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"n_features\",\"t\":\"num\",\"w\":0.5,\"h\":[\"13ce5d9ff943ae3b283c\",\"e5bf55ba0a3a576060bf\",\"281f893e6234c82225e6\"]},{\"kind\":\"scalar\",\"var\":\"n_train\",\"t\":\"num\",\"w\":0.5,\"h\":[\"2cd87e09586d3b4e6f1f\",\"544b0e143d0d5d0c0e6d\",\"e9f2b04f52447f80c4bb\"]},{\"kind\":\"scalar\",\"var\":\"n_val\",\"t\":\"num\",\"w\":0.5,\"h\":[\"1b81472dc9c4a2e0d32b\",\"f428f4a02c8ce22f9e08\",\"beed223641d3031cba93\"]},{\"kind\":\"scalar\",\"var\":\"target_in_features\",\"t\":\"bool\",\"h\":[\"45f35146032c5194c5c9\"]}]},\"Q4.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_1\",\"min_words\":25}]},\"K4.1\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_1\",\"h\":\"310a25a87dc7234e81ec\"}]},\"4.2\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"baseline_rmse\",\"t\":\"num\",\"w\":0.001,\"h\":[\"a125a99f56b498514588\",\"d21a6d222b370013e4f1\",\"16d947b6fc29948031a2\"]},{\"kind\":\"scalar\",\"var\":\"baseline_r2\",\"t\":\"num\",\"w\":0.001,\"h\":[\"b30839c610ecb6bb9c70\",\"2a185635eeb058ca98e2\",\"7831340ad0c0810ecfb7\"]}]},\"4.3\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"linear_rmse\",\"t\":\"num\",\"w\":0.001,\"h\":[\"99fc066f99ce0c180bb8\",\"6e45560fd630363aea4d\",\"c9d19cbc1bb6045c7534\"]},{\"kind\":\"scalar\",\"var\":\"linear_r2\",\"t\":\"num\",\"w\":0.001,\"h\":[\"be3cf0abe68cf7196e07\",\"c3ce0bf5e7e15e1576b6\",\"0662413a1b3d3f80d578\"]}]},\"Q4.2\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_2\",\"min_words\":25}]},\"K4.2\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_2\",\"h\":\"72a088640a9c67817775\"}]},\"4.4\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"ridge_cv_mean\",\"t\":\"num\",\"w\":0.001,\"h\":[\"b7ae9523e9d30220cda8\",\"1f6399dab5bc1157933e\",\"87258cd36da538181c88\"]},{\"kind\":\"list_close\",\"var\":\"ridge_cv_scores\",\"w\":0.001,\"s\":[[\"bb339253a09a115192f1\",\"b6ccbac3b5f1dd6ce0e3\",\"dd87a97cd6bdac178f35\"],[\"f0b18878211d83adc4d7\",\"a3ebd37565d3b57059e4\",\"f00469e595e7f669cc45\"],[\"8e9b72ad4e115d67fcc7\",\"3a69a3375d187e99ee56\",\"40c04b80eba5447f6eb7\"],[\"f372b6d3a56f3c916d3a\",\"e8caa67ef613af37cf95\",\"116eddb5b725667199ae\"],[\"1005a2e973ea3549d6e5\",\"71bf0e3a3e931c57af55\",\"cec20c4562426cfa7c84\"]]}]},\"Q4.3\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_3\",\"min_words\":25}]},\"K4.3\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_3\",\"h\":\"82fc26bd5355ac026595\"}]},\"4.5\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"forest_val_rmse\",\"t\":\"num\",\"w\":0.05,\"h\":[\"d2de0d33939f1911499a\",\"676f1b2926ec6848a9bb\",\"878bfe0e167b3367175e\"]},{\"kind\":\"scalar\",\"var\":\"forest_train_rmse\",\"t\":\"num\",\"w\":0.05,\"h\":[\"c8eeb184861df12a2aa8\",\"a53b5384f98df753ec1f\",\"bf9fa618c199fec4f5d5\"]}]},\"Q4.4\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_4\",\"min_words\":25}]},\"K4.4\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_4\",\"h\":\"f164ec602fdf5f93e039\"}]},\"4.6\":{\"items\":[{\"kind\":\"dict_close\",\"var\":\"val_rmse\",\"w\":0.15,\"s\":{\"Linear\":[\"48e35ba04fefcd7fb970\",\"98e18895c78e334d017e\",\"2e4c386bf8ab09db4178\"],\"Ridge\":[\"48e35ba04fefcd7fb970\",\"98e18895c78e334d017e\",\"2e4c386bf8ab09db4178\"],\"Lasso\":[\"48e35ba04fefcd7fb970\",\"98e18895c78e334d017e\",\"2e4c386bf8ab09db4178\"],\"Forest\":[\"2e4c386bf8ab09db4178\",\"df3161058c2e08593d9f\",\"80d2de095d86f0f12d82\"],\"Boosting\":[\"2e4c386bf8ab09db4178\",\"df3161058c2e08593d9f\",\"80d2de095d86f0f12d82\"]}},{\"kind\":\"self\",\"var\":\"best_name\"}]},\"Q4.5\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_5\",\"min_words\":25}]},\"K4.5\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_5\",\"h\":\"0bd2796f37cd09bfcd97\"}]},\"4.7\":{\"items\":[{\"kind\":\"list_eq\",\"var\":\"top3\",\"h\":\"e0a920a31695236a99f3\"},{\"kind\":\"scalar\",\"var\":\"n_zero_ish\",\"t\":\"num\",\"w\":0.5,\"h\":[\"8bc26da3a499f7cc8067\",\"73ba998ed13cd73a6a17\",\"a8c0ce4f587267652309\"]}]},\"Q4.6\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_6\",\"min_words\":25}]},\"K4.6\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_6\",\"h\":\"7d85636371100935c630\"}]},\"4.8\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"mae_high\",\"t\":\"num\",\"w\":0.05,\"h\":[\"34666479dd0cdf0b4c4b\",\"6ce5ba6fb9242e77a88b\",\"1e68baa30bbde125481f\"]},{\"kind\":\"scalar\",\"var\":\"mae_normal\",\"t\":\"num\",\"w\":0.05,\"h\":[\"11fae85beed6cea72e94\",\"515268fee0af8adea81f\",\"29ca451d35f2fbe829dc\"]},{\"kind\":\"scalar\",\"var\":\"bias_high\",\"t\":\"num\",\"w\":0.05,\"h\":[\"a43ea1201a26c1158db0\",\"76715e57a76c376dfc27\",\"1671f15b027661810489\"]}]},\"Q4.7\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_7\",\"min_words\":25}]},\"K4.7\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_7\",\"h\":\"8fab64aa19643430f978\"}]},\"4.9\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"rmse_primary\",\"t\":\"num\",\"w\":0.001,\"h\":[\"e017c8123169fa8e5263\",\"f049c7e87403df066f02\",\"ee0ed0a3466bbb5ab4f5\"]},{\"kind\":\"scalar\",\"var\":\"rmse_with_bpmeds\",\"t\":\"num\",\"w\":0.001,\"h\":[\"eb531a16230b1061cfc9\",\"55b0c1d43866a7ec34be\",\"fd449c43a4b8a6bc20a2\"]},{\"kind\":\"scalar\",\"var\":\"rmse_change\",\"t\":\"num\",\"w\":0.001,\"h\":[\"a04235f4ef8ea9f57351\",\"06a112e1d3a45544279e\",\"515b2712af8a383b52e5\"]}]},\"Q4.8\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_8\",\"min_words\":25}]},\"K4.8\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_8\",\"h\":\"1638ec0c56ffc17bea96\"}]},\"4.10\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"test_rmse\",\"t\":\"num\",\"w\":0.001,\"h\":[\"5621a6eaa1b904e19cc0\",\"6be3bd01c4e3c7162252\",\"bb7333d1978d1a72ae9a\"]},{\"kind\":\"scalar\",\"var\":\"test_mae\",\"t\":\"num\",\"w\":0.001,\"h\":[\"c850375198b6600788a0\",\"45c640fdf527289a2c1e\",\"56c8bc9cc3b2476a6488\"]},{\"kind\":\"scalar\",\"var\":\"test_r2\",\"t\":\"num\",\"w\":0.001,\"h\":[\"48c5d8821673b97deb99\",\"02e0101c170c6944a669\",\"1ba217f09d2a7c310772\"]},{\"kind\":\"scalar\",\"var\":\"generalisation_gap\",\"t\":\"num\",\"w\":0.001,\"h\":[\"4fc9c99152424d37dd4a\",\"19b274669961933ce1e2\",\"54c62e1b53d7ceb41c5a\"]}]},\"Q4.9\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_9\",\"min_words\":25}]},\"K4.9\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_4_9\",\"h\":\"5122f57a5986902d3aca\"}]},\"Q4.10\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_4_10\",\"min_words\":25}]},\"R4.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"research_4_1_summary\",\"min_words\":40}]},\"5.1\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"prev_train\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"7a2808b57e37fbb3f06b\",\"9bff93a2b42c6ffad972\",\"9f2de44e4c146929ed23\"]},{\"kind\":\"scalar\",\"var\":\"n_pos_val\",\"t\":\"num\",\"w\":0.5,\"h\":[\"92da71e21de95f9b2a44\",\"72c004db1fa3edb7eb6b\",\"253ab44d81b885b3e6e6\"]},{\"kind\":\"scalar\",\"var\":\"acc_always_zero\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"cf86a924a94b6e3629cd\",\"f1dea03c0f4368c34902\",\"06162f11d1784d9e6eb2\"]}]},\"5.2\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"dummy_accuracy\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"cf86a924a94b6e3629cd\",\"f1dea03c0f4368c34902\",\"06162f11d1784d9e6eb2\"]},{\"kind\":\"scalar\",\"var\":\"dummy_recall\",\"t\":\"num\",\"w\":1e-09,\"h\":[\"fa567cbb97f07e4569a8\",\"f4626b0548a8c8ff62d3\",\"69625a8de0be7452e260\"]}]},\"Q5.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_1\",\"min_words\":25}]},\"K5.1\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_1\",\"h\":\"9bd6010fe86cbf9ad4eb\"}]},\"5.3\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"logit_auc\",\"t\":\"num\",\"w\":0.001,\"h\":[\"2f26b842bdbd3cd8ceef\",\"d0d4986b8162d336e828\",\"d7bdbf55db20990c53af\"]},{\"kind\":\"scalar\",\"var\":\"logit_prauc\",\"t\":\"num\",\"w\":0.001,\"h\":[\"0100e9cba5a9ac9e1267\",\"6ee30cb169c2db8f711c\",\"21af888aaab6d0989310\"]},{\"kind\":\"scalar\",\"var\":\"logit_brier\",\"t\":\"num\",\"w\":0.001,\"h\":[\"af799cb109d8cf7767d9\",\"492ea83807d3ff3f70d0\",\"5e72e3611578a3e57286\"]}]},\"5.4\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"logit_cv_mean\",\"t\":\"num\",\"w\":0.001,\"h\":[\"defaa4755d613358a3b4\",\"2e5eea1d4ce78dd4beb9\",\"0ad4a1d7276844a63b67\"]},{\"kind\":\"list_close\",\"var\":\"logit_cv_scores\",\"w\":0.001,\"s\":[[\"1a6abdefa6e87a10977a\",\"a51efd5494f9e10dc6be\",\"56a731ffd193235ce119\"],[\"d9b5d1aaa581e5648487\",\"bc65dea77580c3cc1152\",\"917834559d0568285cc0\"],[\"d7bdbf55db20990c53af\",\"5bd38b4b6afa32cc9e56\",\"ff36144147a3bec35dd2\"],[\"a1739f2150265f678ee7\",\"d80b53a2ca8ae96eac41\",\"cc8021c9d3203c929893\"],[\"0b0b28daed8f16ae8768\",\"5a95c45d64743aae2fba\",\"d9b5d1aaa581e5648487\"]]}]},\"Q5.2\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_2\",\"min_words\":25}]},\"K5.2\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_2\",\"h\":\"314bb5e875dca43b474f\"}]},\"5.5\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"tn\",\"t\":\"num\",\"w\":0.5,\"h\":[\"54d809de8f03fd1d7437\",\"98eb6e066b87babfd6e0\",\"8a2e4d6e58c3e6d494c0\"]},{\"kind\":\"scalar\",\"var\":\"fp\",\"t\":\"num\",\"w\":0.5,\"h\":[\"c44beb2c636975def71e\",\"1c9a5aec00973e29988c\",\"c1d646f03a61d18ba4b6\"]},{\"kind\":\"scalar\",\"var\":\"fn\",\"t\":\"num\",\"w\":0.5,\"h\":[\"115a6ae61c47b4810c54\",\"0fb390ded6df97a034ab\",\"777d0494b07a4b89e226\"]},{\"kind\":\"scalar\",\"var\":\"tp\",\"t\":\"num\",\"w\":0.5,\"h\":[\"7fb6f7a0bf10def8ae14\",\"b535ce720fed5f19e313\",\"11df4e81d0b67f94362b\"]},{\"kind\":\"scalar\",\"var\":\"recall_bal\",\"t\":\"num\",\"w\":0.001,\"h\":[\"e1767196e79deeb0c71c\",\"6a09a7ceb5f597de9894\",\"6cf0ba2c9b10860db06e\"]},{\"kind\":\"scalar\",\"var\":\"precision_bal\",\"t\":\"num\",\"w\":0.001,\"h\":[\"11d5466249ac55c44bde\",\"9586286103cca0416338\",\"8b52303607d6fec3fe61\"]}]},\"Q5.3\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_3\",\"min_words\":25}]},\"K5.3\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_3\",\"h\":\"c5a83bd3f1c329158546\"}]},\"5.6\":{\"items\":[{\"kind\":\"dict_close\",\"var\":\"val_auc\",\"w\":0.03,\"s\":{\"Logistic\":[\"e432ef8cc6868fc52ca0\",\"c4e66d14965aa75f2f61\",\"a3b4b1157ff1358fc149\"],\"Forest\":[\"1dca4909f628aaa7dac2\",\"e432ef8cc6868fc52ca0\",\"c4e66d14965aa75f2f61\"],\"Boosting\":[\"1dca4909f628aaa7dac2\",\"e432ef8cc6868fc52ca0\",\"c4e66d14965aa75f2f61\"]}},{\"kind\":\"self\",\"var\":\"best_family\"}]},\"Q5.4\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_4\",\"min_words\":25}]},\"K5.4\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_4\",\"h\":\"2f713bdd5138e4317339\"}]},\"5.7\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"tuned_auc\",\"t\":\"num\",\"w\":0.01,\"h\":[\"62bd5b0855d75750a9f0\",\"8d30e724ba8947ddb3a5\",\"081b2126e5907c487bb2\"]},{\"kind\":\"self\",\"var\":\"tuned_C\"}]},\"Q5.5\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_5\",\"min_words\":25}]},\"K5.5\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_5\",\"h\":\"21994f7bb8355df9cfd8\"}]},\"5.8\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"best_thr\",\"t\":\"num\",\"w\":0.02,\"h\":[\"a44c30779dff30e91785\",\"09fb853b06aa7b559ccf\",\"a27c1a44df50cd8f70cf\"]},{\"kind\":\"scalar\",\"var\":\"f1_at_best\",\"t\":\"num\",\"w\":0.02,\"h\":[\"228a0497c4456d1d3cc6\",\"6a727f2a0a583ca14581\",\"ea91b0da460ad46890bb\"]},{\"kind\":\"scalar\",\"var\":\"recall_at_best\",\"t\":\"num\",\"w\":0.03,\"h\":[\"c4e66d14965aa75f2f61\",\"a3b4b1157ff1358fc149\",\"1a958bad9ea2c969198b\"]},{\"kind\":\"scalar\",\"var\":\"precision_at_best\",\"t\":\"num\",\"w\":0.03,\"h\":[\"8aa4d9fceb000ec092d7\",\"85d1ed3a3b33fa82266e\",\"2d696fc978bb9567ad9a\"]}]},\"Q5.6\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_6\",\"min_words\":25}]},\"K5.6\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_6\",\"h\":\"37c1c3555c313db4ed55\"}]},\"5.9\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"mean_pred_unw\",\"t\":\"num\",\"w\":0.001,\"h\":[\"e30f5b56fcb4908ec30c\",\"3998e96bd23dd96ee764\",\"216b2143ad8cb78ad381\"]},{\"kind\":\"scalar\",\"var\":\"mean_pred_bal\",\"t\":\"num\",\"w\":0.001,\"h\":[\"3454141801e25ee13b32\",\"98405a63aa77ee603659\",\"40fcb3bd218ff1df845a\"]},{\"kind\":\"scalar\",\"var\":\"prev_val\",\"t\":\"num\",\"w\":1e-06,\"h\":[\"7720f6072a1d3fb60922\",\"6ca6fee273a735f192fc\",\"dce1a94ba3293f3963d9\"]}]},\"Q5.7\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_7\",\"min_words\":25}]},\"K5.7\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_7\",\"h\":\"5ac2eccca7b9615d7fe5\"}]},\"5.10\":{\"items\":[{\"kind\":\"list_eq\",\"var\":\"top3_chd\",\"h\":\"2f3e033f0a207b61c132\"},{\"kind\":\"scalar\",\"var\":\"age_auc_drop\",\"t\":\"num\",\"w\":0.01,\"h\":[\"062f772d3f072c938952\",\"171841d075237d324afc\",\"4ea27e7e2c609b614deb\"]}]},\"Q5.8\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_8\",\"min_words\":25}]},\"K5.8\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_8\",\"h\":\"ce99cb56d17756479995\"}]},\"5.11\":{\"items\":[{\"kind\":\"scalar\",\"var\":\"test_auc\",\"t\":\"num\",\"w\":0.005,\"h\":[\"aa322c483c73dc680606\",\"2bad1a9ea8a14d786d57\",\"80e03256673cc7a7f2e3\"]},{\"kind\":\"scalar\",\"var\":\"test_recall\",\"t\":\"num\",\"w\":0.02,\"h\":[\"5a635208e5bc0048411f\",\"5d856dcc925855db54e2\",\"a5ef99d05c9dbf65936e\"]},{\"kind\":\"scalar\",\"var\":\"test_precision\",\"t\":\"num\",\"w\":0.02,\"h\":[\"3d6012a8859a5e93ac60\",\"dbec3b2b6c505c79628e\",\"798c5e62c0827151c2b0\"]},{\"kind\":\"scalar\",\"var\":\"test_f1\",\"t\":\"num\",\"w\":0.02,\"h\":[\"a3d5292f717c17b0a039\",\"52899fed29faedb3286c\",\"228a0497c4456d1d3cc6\"]},{\"kind\":\"scalar\",\"var\":\"auc_gap\",\"t\":\"num\",\"w\":0.01,\"h\":[\"6c135414bae6f8e4cdd2\",\"41cb08b366f428595820\",\"0e50cfffd1447cc6e29f\"]}]},\"Q5.9\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_9\",\"min_words\":25}]},\"K5.9\":{\"items\":[{\"kind\":\"mcq\",\"var\":\"kc_5_9\",\"h\":\"20abc4e3f675b3ed0aa5\"}]},\"Q5.10\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_10\",\"min_words\":25}]},\"Q5.11\":{\"items\":[{\"kind\":\"written\",\"var\":\"answer_5_11\",\"min_words\":25}]},\"R5.1\":{\"items\":[{\"kind\":\"written\",\"var\":\"research_5_1_summary\",\"min_words\":40}]}}}")

_results, _written, _tries = {}, {}, {}


# ---------------------------------------------------------------- fingerprints
def _h(text):
    return hashlib.sha256((_SALT + "|" + text).encode("utf-8")).hexdigest()[:20]


def _is_num(x):
    try:
        import numpy as np
        return isinstance(x, (numbers.Number, np.number)) and not isinstance(x, (bool, np.bool_))
    except Exception:
        return isinstance(x, numbers.Number) and not isinstance(x, bool)


def _nset(x, w):
    """Fingerprints of the bucket of x and its two neighbours (so values within the tolerance still match)."""
    x = float(x)
    if math.isnan(x):
        return [_h("nan")]
    b = math.floor(x / w + 0.5)
    return [_h(f"n|{w}|{k}") for k in (b - 1, b, b + 1)]


def _num_ok(val, hashes, w):
    """The value's own bucket must be one of the stored fingerprints (the answer's bucket and its two neighbours)."""
    if not _is_num(val):
        return False
    x = float(val)
    if math.isnan(x):
        return _h("nan") in hashes
    return _h(f"n|{w}|{math.floor(x / w + 0.5)}") in hashes


def _jlist(seq):
    return json.dumps([str(x) for x in seq])


# ---------------------------------------------------------------- reading the notebook
def _user_ns():
    ip = get_ipython() if get_ipython else None
    return ip.user_ns if ip is not None else globals()


def _source_of(ex, ns):
    import re
    tag = f"# [Exercise {ex}]"
    cells = [c for c in (ns.get("In") or []) if isinstance(c, str) and c.lstrip().startswith(tag)]
    src = "\n".join(cells)
    return "\n".join(line.split("#")[0] for line in src.splitlines()).lower()


def _short(v):
    try:
        if _is_num(v):
            return f"{float(v):.6g}"
    except Exception:
        pass
    t = repr(v).replace("\n", " ")
    return t if len(t) <= 60 else t[:57] + "..."


# ---------------------------------------------------------------- one item
def _run_item(it, ns, ex):
    kind, var = it["kind"], it.get("var")

    if kind == "source_has":
        src = _source_of(ex, ns)
        miss = [w for w in it["words"] if w.lower() not in src]
        if not src.strip():
            return False, "I could not find your exercise cell. Run the exercise cell first, then this check."
        if miss:
            return False, "Your code is missing: " + ", ".join(f"`{m}`" for m in miss) + "."
        return True, "your chart has all the required parts."

    if var not in ns:
        return False, f"`{var}` is not defined yet. Run the cell above it first."
    v = ns[var]

    if kind == "written":
        text = str(v or "").strip()
        n = len(text.split())
        if n == 0:
            return False, f"`{var}` is still empty. Write your answer between the triple quotes."
        if n < it["min_words"]:
            return False, f"`{var}` is a little short ({n} words). Aim for at least {it['min_words']} words."
        return True, f"answer saved ({n} words). Your teacher will read it."

    if kind == "mcq":
        s = str(v).strip().upper()
        if s not in ("A", "B", "C", "D"):
            return False, f"`{var}` should be a single letter: A, B, C or D."
        ok = _h(f"mcq|{var}|{s}") == it["h"]
        return ok, f"`{var}`: " + ("correct!" if ok else "not this one. Re-read the question and the options.")

    if v is None:
        return False, f"`{var}` is still `None`. Replace the blank with your own code and run the exercise cell again."

    if kind == "self":
        try:
            own = {"best_name": lambda: min(ns["val_rmse"], key=ns["val_rmse"].get),
                   "best_family": lambda: max(ns["val_auc"], key=ns["val_auc"].get),
                   "tuned_C": lambda: ns["search"].best_params_["model__C"]}[var]()
            ok = (v == own)
        except Exception:
            return False, f"`{var}` needs the tables from the exercises above. Run them first."
        return ok, f"`{var}`: " + ("correct!" if ok else "it should match your own table above.")

    try:
        ok, why = _compare(it, v)
    except Exception as e:                                       # wrong type etc. is just "not yet"
        return False, f"`{var}`: I could not compare it ({type(e).__name__}). Check the type of your value."
    if ok:
        return True, f"`{var}`: correct!"
    return False, f"`{var}`: not quite yet. {why}"


def _compare(it, v):
    import pandas as pd
    kind, w = it["kind"], it.get("w")
    shown = f"Your value is {_short(v)}."

    if kind == "scalar":
        t = it["t"]
        if t == "bool":
            ok = isinstance(v, bool) or type(v).__name__ == "bool_"
            return ok and _h(f"b|{bool(v)}") == it["h"][0], shown
        if t == "num":
            if not _is_num(v):
                return False, "It should be a number. " + shown
            return _num_ok(v, it["h"], w), shown
        return _h(f"s|{v}") == it["h"][0], shown

    if kind == "rows":
        n = len(v) if hasattr(v, "__len__") else v
        return _num_ok(n, it["h"], w), f"Your count is {_short(n)}."

    if kind == "columns":
        return _h("l|" + _jlist(v.columns)) == it["h"], "Check the column names and their order."

    if kind == "list_eq":
        return _h("l|" + _jlist(v)) == it["h"], "Check the items and their order."

    if kind == "set_eq":
        return _h("e|" + _jlist(sorted(set(map(str, v))))) == it["h"], "Check which items are included."

    if kind == "list_close":
        vals = list(v)
        ok = len(vals) == len(it["s"]) and all(_num_ok(x, hs, w) for x, hs in zip(vals, it["s"]))
        return ok, f"Expected {len(it['s'])} values; you have {len(vals)}." if len(vals) != len(it["s"]) else "Some values differ."

    if kind == "series_close":
        s = pd.Series(v).sort_index()
        if _h("i|" + _jlist(s.index)) != it["i"]:
            return False, "The labels (index) differ from what is expected."
        vals = list(s.values)
        ok = len(vals) == len(it["s"]) and all(_num_ok(x, hs, w) for x, hs in zip(vals, it["s"]))
        return ok, "Some values differ."

    if kind == "dict_close":
        if set(map(str, v)) != set(it["s"]):
            return False, "The keys differ from what is expected: " + ", ".join(sorted(it["s"])) + "."
        d = {str(k): x for k, x in v.items()}
        return all(_num_ok(d[k], hs, w) for k, hs in it["s"].items()), "Some values differ."

    if kind in ("func", "func_series"):
        if not callable(v):
            return False, "It should be a function."
        passed = 0
        for args, want in it["tests"]:
            try:
                got = v(*args)
                if want["t"] == "none":
                    passed += got is None
                elif want["t"] == "num":
                    passed += _num_ok(got, want["h"], w)
                else:
                    passed += _h(f"s|{got}") == want["h"][0]
            except Exception:
                pass
        n = len(it["tests"])
        return passed == n, f"Your function gave the right result for {passed} of {n} hidden test inputs."

    return False, "Unknown check type."


# ---------------------------------------------------------------- public API
def check(ex):
    """Check exercise `ex` (for example check("2.14")). A failed check never stops the notebook."""
    try:
        spec = SPEC["items"].get(ex)
        if spec is None:
            print(f"⚠️ I do not know an exercise called {ex!r}. Check the number in the cell.")
            return
        ns = _user_ns()
        all_ok, written = True, ex[0] in "QR"
        for it in spec["items"]:
            ok, msg = _run_item(it, ns, ex)
            all_ok = all_ok and ok
            icon = ("📝 " if ok else "✍️ ") if written else ("✅ " if ok else "❌ ")
            print(icon + msg)
        if written:
            _written[ex] = all_ok
            return
        _results[ex] = all_ok
        if not all_ok:
            _tries[ex] = _tries.get(ex, 0) + 1
            hint = spec.get("hint") or "Re-read the LEARN and SEE cells just above this exercise, then try again."
            if _tries[ex] >= 2 or not spec.get("hint"):
                print("💡 Hint:", hint)
            if _tries[ex] >= 3:
                print("🤝 Still stuck? Look at the worked example above this exercise, or ask your teacher.")
    except Exception as e:                                       # a checker problem must never break a notebook
        print(f"⚠️ The checker had a problem ({type(e).__name__}). Your notebook is fine; tell your teacher.")


def progress(nb):
    """Summary of the checks you have run in this notebook."""
    nb = str(nb)
    ids = [k for k in SPEC["items"] if k.lstrip("KQR").split(".")[0] == nb]
    ex = [k for k in ids if k[0] not in "KQR"]
    kc = [k for k in ids if k[0] == "K"]
    wr = [k for k in ids if k[0] in "QR"]
    done = lambda ks: [k for k in ks if _results.get(k)]
    print(f"Notebook {nb} progress")
    print(f"  Exercises passed:           {len(done(ex))} of {len(ex)}")
    print(f"  Knowledge checks correct:   {len(done(kc))} of {len(kc)}")
    print(f"  Written answers completed:  {sum(bool(_written.get(k)) for k in wr)} of {len(wr)}  (your teacher reads these)")
    failed = [k for k in ex + kc if k in _results and not _results[k]]
    todo = [k for k in ex + kc if k not in _results]
    if failed:
        print("  Run but not passed yet:", ", ".join(failed))
    if todo:
        print("  Not checked yet:", ", ".join(todo))
    if not failed and not todo and all(_written.get(k) for k in wr):
        print("🎉 Everything is complete. Save your notebook with your name in the filename.")
    print("  (Feedback only. Your instructor's marking is separate.)")
