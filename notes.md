# System Design & Tech Notes

> Auto-generated summaries from articles. Last updated: 2026-08-06.

## Table of Contents

<!-- INDEX START -->
- [Medium](#medium) — *2026-08-06 01:22*
<!-- INDEX END -->

---


## Medium

*Added: 2026-08-06 01:22*

**Source:** [https://medium.com/@saudanwar17/latency-throughput-and-availability-966b2f1b5b75](https://medium.com/@saudanwar17/latency-throughput-and-availability-966b2f1b5b75)

## Overview

Latency, throughput, and availability are fundamental concepts in system design, acting as the core pillars of a system's performance. Balancing these three aspects is crucial for building services that are responsive, scalable, and reliable for users.

### Latency

Latency measures the time it takes for a single request to complete a round trip from client to server and back. It is typically measured in milliseconds (ms). A system with low latency responds quickly, which is desirable for a smooth user experience. For example, reading data from RAM has much lower latency than reading from an HDD.

### Throughput

Throughput refers to the number of successful requests or units of work a system can handle per second. It is commonly measured in requests per second (RPS) or transactions per second (TPS). High throughput indicates a system can process a large volume of work efficiently. Examples include network data transfer rates or how many tasks a CPU can complete per second.

### Availability

Availability describes a system's readiness and accessibility to users at any given moment. It is often expressed as a percentage, calculated by dividing the total operational time (uptime) by the sum of uptime and downtime. High availability means the system is consistently operational and accessible, minimizing interruptions for users.

### Conclusion

An ideal system strives for a combination of high throughput (handling many requests), high availability (always being accessible), and low latency (responding quickly).

---
