INVALID_SIGN = (
    401,
    "Invalid signature detected. The provided signature does not match the expected value."
)

ACCESS_DENIED = (
    403,
    "Access denied due to invalid IP address."
)

INVOICE_NOT_FOUND = (
    404,
    "The requested invoice ID does not exist or has been deleted."
)

AMOUNT_NOT_SATISFIED = (
    422,
    "The specified amount does not meet the required criteria."
)

SUCCESS = (
    200,
    "The request has been processed successfully."
)
