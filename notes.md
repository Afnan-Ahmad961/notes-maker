# System Design & Tech Notes

> Auto-generated summaries from articles. Last updated: 2026-08-06.

## Table of Contents

<!-- INDEX START -->
- [Latency, Throughput And Availability](#latency-throughput-and-availability) — *2026-08-06 01:28*
- [Horizontal and Vertical Scaling | System Design](#horizontal-and-vertical-scaling-system-design) — *2026-08-06 01:44*
<!-- INDEX END -->

---


## Latency, Throughput And Availability

*Added: 2026-08-06 01:28*

**Source:** [https://medium.com/@saudanwar17/latency-throughput-and-availability-966b2f1b5b75](https://medium.com/@saudanwar17/latency-throughput-and-availability-966b2f1b5b75)

## Overview
This article explains three fundamental concepts in system design: latency, throughput, and availability. It highlights their importance in building responsive, scalable, and reliable services, emphasizing the goal of achieving low latency, high throughput, and high availability.

## Latency
Latency refers to the time it takes for a single request or unit of work to complete, typically measured in milliseconds. A system with low latency responds quickly, which is desirable for a good user experience. For example, reading data from RAM has much lower latency than reading from an HDD.

## Throughput
Throughput measures the number of successful requests or units of work a system can handle per second, often expressed as requests per second (RPS) or transactions per second (TPS). High throughput indicates a system's capacity to process a large volume of operations efficiently. Throughput applies to various contexts, including network data transfer, disk read/write speeds, and CPU processing capabilities.

## Availability
Availability describes a system's readiness and accessibility to users at any given moment. It is calculated as the percentage of time a system is operational (uptime) compared to its total operational and downtime. High availability ensures that users can consistently access and use the system without interruptions due to failures or maintenance.

---

## Horizontal and Vertical Scaling | System Design

*Added: 2026-08-06 01:44*

**Source:** [https://www.geeksforgeeks.org/system-design/system-design-horizontal-and-vertical-scaling/](https://www.geeksforgeeks.org/system-design/system-design-horizontal-and-vertical-scaling/)

## Overview
This article explains two fundamental approaches to scaling a system: vertical scaling (scaling up) and horizontal scaling (scaling out). Both methods aim to improve system performance and capacity to handle increased user loads and data, with each having distinct advantages and disadvantages depending on the application's needs.

## Why Scaling is Needed
Scaling is essential for systems to efficiently manage growing user traffic and data. It ensures high availability, maintains consistent performance and response times, and prevents system slowdowns or crashes during peak usage.

## Vertical Scaling (Scaling Up)
### Concept
Vertical scaling involves increasing the resources of a single server or machine. This means upgrading components like the CPU, RAM, or storage of an existing system to enhance its capacity and performance. It's often simpler to implement and suitable for smaller applications or monolithic architectures.

### Advantages
*   **Increased Capacity:** Directly boosts the performance of a single server.
*   **Easier Management:** Involves managing and upgrading fewer individual components.

### Disadvantages
*   **Hardware Limitations:** Restricted by the maximum capacity of a single machine.
*   **Single Point of Failure:** If the upgraded server fails, the entire system can go down.
*   **Downtime:** Upgrades often require the server to be restarted or replaced, causing service interruptions.

## Horizontal Scaling (Scaling Out)
### Concept
Horizontal scaling involves adding more servers or machines to a system and distributing the workload across them. Instead of making one server more powerful, you add more servers to share the load, increasing overall capacity and resilience.

### Advantages
*   **Increased Capacity:** Allows for virtually limitless scaling by adding more nodes.
*   **Improved Performance:** Distributes the workload, preventing any single server from becoming overloaded.
*   **Increased Fault Tolerance:** If one server fails, others can continue to handle requests, reducing downtime.

### Disadvantages
*   **Complex Architecture:** Requires additional components like load balancers and distributed databases.
*   **Consistency Challenges:** Maintaining data consistency across multiple distributed nodes can be difficult.
*   **Higher Operational Costs:** More machines mean increased costs for networking, power, and maintenance.
*   **Management Complexity:** Requires orchestration tools to manage a large number of servers effectively.

## Choosing a Scaling Approach
The decision between horizontal and vertical scaling, or often a hybrid approach, depends on specific system requirements, business goals, and architectural considerations. Many large organizations combine aspects of both to leverage the speed and consistency of vertical scaling with the resilience and extensive scalability of horizontal scaling.

---
