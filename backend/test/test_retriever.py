from app.core.retriever import cosine_similarity


def test_cosine_similarity():
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    vec3 = [0.0, 1.0, 0.0]

    assert (
        cosine_similarity(vec1, vec2) == 1.0
    ), "Identical vectors should have similarity 1.0"
    assert (
        cosine_similarity(vec1, vec3) == 0.0
    ), "Orthogonal vectors should have similarity 0.0"

    vec4 = [0.5, 0.5, 0.0]
    assert (
        round(cosine_similarity(vec1, vec4), 2) == 0.5
    ), "Half-aligned vector should return ~0.5"


if __name__ == "__main__":
    test_cosine_similarity()
    print("All tests passed!")
