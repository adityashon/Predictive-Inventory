  # Query for shopify

ORDERS_QUERY = """
query Orders($first: Int!, $after: String) {
    orders(first: $first, after: $after) {
        nodes {
            id
            name
            createdAt

            fulfillments(first: 1) {
                location {
                    id
                    name
                }
            }

            lineItems(first: 100) {
                nodes {
                    quantity

                    variant {
                        sku
                    }

                    originalUnitPriceSet {
                        shopMoney {
                            amount
                            currencyCode
                        }
                    }
                }
            }
        }

        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
"""