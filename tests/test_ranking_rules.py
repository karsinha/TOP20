import pytest

from app.services.ranking_rules import (
    InvalidRankingError,
    effective_positions,
    tail_position,
    validate_ranking,
)

POOL = set(range(1, 26))  # 25 clubs, ids 1..25
RANKING_SIZE = 20


def valid_ranking() -> list[int]:
    return list(range(1, 21))


def test_valid_ranking_passes():
    validate_ranking(valid_ranking(), POOL, RANKING_SIZE)


def test_empty_ranking_is_rejected():
    with pytest.raises(InvalidRankingError):
        validate_ranking([], POOL, RANKING_SIZE)


def test_too_few_clubs_is_rejected():
    with pytest.raises(InvalidRankingError):
        validate_ranking(list(range(1, 20)), POOL, RANKING_SIZE)


def test_too_many_clubs_is_rejected():
    with pytest.raises(InvalidRankingError):
        validate_ranking(list(range(1, 22)), POOL, RANKING_SIZE)


def test_duplicate_club_is_rejected():
    ranking = valid_ranking()
    ranking[5] = ranking[0]
    with pytest.raises(InvalidRankingError):
        validate_ranking(ranking, POOL, RANKING_SIZE)


def test_club_outside_pool_is_rejected():
    ranking = valid_ranking()
    ranking[0] = 999
    with pytest.raises(InvalidRankingError):
        validate_ranking(ranking, POOL, RANKING_SIZE)


def test_tail_position_for_pool_of_25():
    assert tail_position(20, 25) == 23


def test_tail_position_for_pool_of_30():
    assert tail_position(20, 30) == 25.5


def test_effective_positions_gives_tail_to_left_out_clubs():
    result = effective_positions(valid_ranking(), POOL, RANKING_SIZE)
    assert len(result) == 25
    assert result[1] == 1
    assert result[20] == 20
    for left_out in range(21, 26):
        assert result[left_out] == 23


def test_effective_positions_keeps_total_constant():
    # Tying the left-out clubs at their average must not change the sum of positions.
    result = effective_positions(valid_ranking(), POOL, RANKING_SIZE)
    assert sum(result.values()) == sum(range(1, 26))