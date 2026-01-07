# Market Mechanics and Matching Engine Design

Modern electronic markets rely on **continuous double-auction mechanisms** to match buyers and sellers efficiently. In this model, participants submit buy (**bid**) and sell (**ask**) orders that specify a price and quantity, or in the case of **market orders**, only a quantity. The exchange maintains an **order book** that aggregates outstanding orders and continuously matches compatible bids and asks.

The primary objectives of such a system are:
- **Price discovery**
- **Fairness**
- **Low-latency execution**

---

## Order Types and Priority Rules

The market supports two fundamental order types:

### Limit Orders
- Specify a price constraint and quantity.
- Rest in the order book until fully executed or canceled.

### Market Orders
- Execute immediately against the best available prices.
- Consume existing liquidity.
- Never rest in the order book.
- Any unfilled quantity is discarded once liquidity is exhausted.

### Price–Time Priority
Matching follows a **strict price–time priority** rule:
1. Orders with **better prices** are matched first.
2. Among orders at the same price, **earlier submissions** have precedence.

This rule ensures fairness and predictability, rewarding participants for competitive pricing and early placement.

---

## Order Book Structure

The order book is divided into two sides:
- **Bids (buy orders)**
- **Asks (sell orders)**

Each side is organized into:
- **Price levels**, indexed by price
- **FIFO queues** at each price level to preserve arrival order

### Key Properties
- Best bid and best ask prices are always directly accessible.
- Bid prices are stored in **descending order**.
- Ask prices are stored in **ascending order**.
- The top of each list represents the best available price.

This structure enables efficient matching while maintaining strict time priority.

---

## Matching and Execution

### Limit Orders
1. Inserted into the order book.
2. Checked for immediate matches against the opposing side.
3. Trades occur if the order price crosses the spread.
4. Matching continues until:
   - The order is fully filled, or
   - No compatible prices remain.

Partial fills are handled by decrementing quantities. Orders are removed only when their quantity reaches zero.

### Market Orders
- Bypass order book insertion entirely.
- Match iteratively against the best available prices on the opposite side.
- Execution stops when:
  - The order is filled, or
  - The order book is empty.

This behavior mirrors real exchange systems and ensures deterministic execution.

---

## Order Management

The system supports the following order lifecycle operations:

### Cancellation
- Removes the order from:
  - Its price-level queue
  - The global order registry
- Ensures no stale references remain.

### Modification
- Updates the remaining quantity of an order.
- Preserves original time priority.
- Reducing quantity does **not** affect priority.
- Setting quantity to zero is treated as a cancellation.

---

## Design Trade-offs

This matching engine prioritizes:
- **Clarity**
- **Correctness**
- **Deterministic behavior**

over extreme micro-optimizations.

### Implementation Choices
- Queues and sorted price lists balance performance and maintainability.
- Avoids complex data structures or hardware acceleration.

While production-grade engines may use specialized trees or FPGA-based components, this design closely reflects real-world exchange logic and is ideal for:
- Simulation
- Research
- Backtesting
- Educational purposes

---

## Conclusion

This matching engine captures the essential mechanics of electronic markets:
- Price–time priority
- Continuous matching
- Robust order management

By adhering to well-established market principles and using simple, reliable data structures, the system provides a faithful and extensible representation of real exchange behavior while remaining accessible for experimentation and analysis.
