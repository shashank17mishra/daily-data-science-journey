import pytest
from learning.python.day_030_rate_limiter import TokenBucketLimiter, MultiClientRateLimiter

class MockClock:
    """A deterministic clock mock to avoid real-world timing issues in tests."""
    def __init__(self, initial_time: float = 1000.0):
        self.current_time = initial_time

    def tick(self, seconds: float = 1.0) -> None:
        self.current_time += seconds

    def __call__(self) -> float:
        return self.current_time


@pytest.fixture
def mock_clock():
    return MockClock()


@pytest.fixture
def basic_limiter(mock_clock):
    # Capacity of 5 tokens, refills at 1 token per second
    return TokenBucketLimiter(capacity=5.0, refill_rate=1.0, time_func=mock_clock)


def test_initial_capacity(basic_limiter):
    """Verify that the bucket starts fully charged."""
    assert basic_limiter.tokens == 5.0


def test_successful_consumption(basic_limiter):
    """Verify that tokens can be consumed successfully."""
    assert basic_limiter.consume(2.0) is True
    assert basic_limiter.tokens == 3.0


def test_failed_consumption_due_to_exhaustion(basic_limiter):
    """Verify consumption fails if requesting more tokens than available."""
    assert basic_limiter.consume(5.0) is True
    assert basic_limiter.consume(1.0) is False


def test_refill_over_time(basic_limiter, mock_clock):
    """Verify that tokens refill correctly as mock time advances."""
    assert basic_limiter.consume(5.0) is True
    assert basic_limiter.consume(1.0) is False
    
    # Advance time by 2 seconds -> should refill 2 tokens
    mock_clock.tick(2.0)
    assert basic_limiter.consume(2.0) is True
    assert basic_limiter.consume(1.0) is False


def test_refill_cap(basic_limiter, mock_clock):
    """Verify that tokens do not exceed the maximum capacity."""
    mock_clock.tick(10.0)  # Refill way past capacity
    assert basic_limiter.consume(5.0) is True
    assert basic_limiter.consume(1.0) is False  # Cannot exceed capacity of 5


@pytest.mark.parametrize(
    "capacity, refill_rate, consume_amount, expected_result",
    [
        (10.0, 2.0, 5.0, True),
        (10.0, 2.0, 11.0, False),
        (1.0, 0.1, 1.0, True),
    ]
)
def test_parameterized_limits(capacity, refill_rate, consume_amount, expected_result, mock_clock):
    """Test various configurations of capacity and consumption amounts."""
    limiter = TokenBucketLimiter(capacity=capacity, refill_rate=refill_rate, time_func=mock_clock)
    assert limiter.consume(consume_amount) is expected_result


def test_invalid_initialization_parameters():
    """Verify that invalid configuration parameters raise ValueErrors."""
    with pytest.raises(ValueError, match="Capacity and refill rate must be strictly positive"):
        TokenBucketLimiter(capacity=-1, refill_rate=1.0)
        
    with pytest.raises(ValueError, match="Capacity and refill rate must be strictly positive"):
        TokenBucketLimiter(capacity=5.0, refill_rate=0.0)


def test_invalid_consumption_value(basic_limiter):
    """Verify that consuming negative tokens raises a ValueError."""
    with pytest.raises(ValueError, match="Cannot consume a negative number of tokens"):
        basic_limiter.consume(-1.0)


def test_multi_client_isolation(mock_clock):
    """Verify that different clients have isolated rate limits."""
    multi_limiter = MultiClientRateLimiter(
        default_capacity=2.0, 
        default_refill_rate=1.0, 
        time_func=mock_clock
    )
    
    # Client A consumes all tokens
    assert multi_limiter.consume("client_A", 2.0) is True
    assert multi_limiter.consume("client_A", 1.0) is False
    
    # Client B should still have full capacity
    assert multi_limiter.consume("client_B", 2.0) is True
