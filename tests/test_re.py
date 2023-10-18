def test_finditer(self):
    iter = re.finditer(r":+", "a:b::c:::d")
    self.assertEqual([item.group(0) for item in iter],
                        [":", "::", ":::"])

    pat = re.compile(r":+")
    iter = pat.finditer("a:b::c:::d", 1, 10)
    self.assertEqual([item.group(0) for item in iter],
                        [":", "::", ":::"])

    pat = re.compile(r":+")
    iter = pat.finditer("a:b::c:::d", pos=1, endpos=10)
    self.assertEqual([item.group(0) for item in iter],
                        [":", "::", ":::"])

    pat = re.compile(r":+")
    iter = pat.finditer("a:b::c:::d", endpos=10, pos=1)
    self.assertEqual([item.group(0) for item in iter],
                        [":", "::", ":::"])

    pat = re.compile(r":+")
    iter = pat.finditer("a:b::c:::d", pos=3, endpos=8)
    self.assertEqual([item.group(0) for item in iter],
                        ["::", "::"])