from ltlf2asp.parser.reify_as_atoms import IDPool


def test_same_object_gets_same_id():
    pool = IDPool()
    i = pool.id((3, 4, 5))
    j = pool.id((3, 4, 5))

    assert i == j


def test_id_increases():
    pool = IDPool()
    i = pool.id("x")
    j = pool.id("y")

    assert i + 1 == j
