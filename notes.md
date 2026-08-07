# System Design & Tech Notes

> Auto-generated summaries from articles. Last updated: 2026-08-06.

## Table of Contents

<!-- INDEX START -->
- [Latency, Throughput And Availability](#latency-throughput-and-availability) — *2026-08-06 01:28*
- [Horizontal and Vertical Scaling | System Design](#horizontal-and-vertical-scaling-system-design) — *2026-08-06 01:44*
- [Describe the CAP theorem and its implications for distributed systems](#describe-the-cap-theorem-and-its-implications-for-distributed-systems) — *2026-08-07 19:41*
- [PACELC Theorem](#pacelc-theorem) — *2026-08-08 00:23*
- [How DNS Works: A Guide to Understanding the Internet's Address Book](#how-dns-works-a-guide-to-understanding-the-internets-address-book) — *2026-08-08 01:40*
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

## Describe the CAP theorem and its implications for distributed systems

*Added: 2026-08-07 19:41*

**Source:** [https://www.geeksforgeeks.org/data-engineering/describe-the-cap-theorem-and-its-implications-for-distributed-systems/](https://www.geeksforgeeks.org/data-engineering/describe-the-cap-theorem-and-its-implications-for-distributed-systems/)

## Overview
The CAP theorem is a foundational principle in distributed systems, stating that it's impossible for a distributed data store to simultaneously guarantee Consistency, Availability, and Partition Tolerance. This theorem guides system designers in making essential trade-offs based on their application's specific needs.

## Understanding the CAP Theorem
Introduced by Eric Brewer, the CAP theorem defines three core properties for distributed systems:

*   **Consistency (C):** Ensures that every read operation receives the most recent write, meaning all nodes in the system see the same data at the same time.
*   **Availability (A):** Guarantees that every request receives a response, even if some nodes fail, ensuring the system remains operational.
*   **Partition Tolerance (P):** Means the system continues to function despite network failures that split the system into isolated groups of nodes.

## The Incompatibility of CAP
The theorem asserts that a distributed system can only achieve two out of these three properties at any given time. This forces designers to choose between:

*   **CP (Consistency and Partition Tolerance):** Systems prioritize data accuracy and can handle network partitions, but may become unavailable during a partition.
*   **AP (Availability and Partition Tolerance):** Systems prioritize continuous operation and can handle network partitions, but may return outdated data, sacrificing immediate consistency.
*   **CA (Consistency and Availability):** While theoretically possible, this combination is impractical in real-world distributed systems because network partitions are inevitable.

## Practical Implications
The CAP theorem profoundly impacts the design of distributed systems:

*   **Design Trade-offs:** Designers must decide whether consistency (e.g., financial transactions) or availability (e.g., online retail) is more critical, as partition tolerance is often a mandatory requirement in distributed environments.
*   **Eventual Consistency:** Many systems adopt eventual consistency, where data will eventually become consistent across all nodes over time, balancing availability with a relaxed form of consistency. Examples include Apache Cassandra (AP) and Apache HBase (CP).

---

## PACELC Theorem

*Added: 2026-08-08 00:23*

**Source:** [https://www.geeksforgeeks.org/operating-systems/pacelc-theorem/](https://www.geeksforgeeks.org/operating-systems/pacelc-theorem/)

## Overview
The PACELC Theorem is an extension of the CAP Theorem, designed to address its limitations by incorporating latency as a critical factor in distributed system design. It provides a framework for making tradeoffs not only during network partitions but also under normal operating conditions.

## Key Concept
The PACELC theorem states that in the event of a **P**artition, a distributed system must choose between **A**vailability and **C**onsistency (P/A or P/C). **E**lse, if there is no partition, the system must choose between **L**atency and **C**onsistency (L/C). This means designers must consider two sets of tradeoffs depending on whether a network partition exists.

## Addressing CAP Theorem's Limitations
The original CAP Theorem did not account for performance or latency when a distributed system was functioning normally (without a network partition). PACELC fills this gap by highlighting that even without partitions, systems must balance the speed of response (latency) with the guarantee of data accuracy (consistency). High latency, even if a system is technically "available," can make it unusable in real-world applications.

## Benefits
The PACELC Theorem offers several advantages:
*   It explicitly considers the crucial tradeoffs between latency and consistency that are always present in distributed systems.
*   It provides a more comprehensive model for designing and choosing appropriate distributed systems.
*   It overcomes a major limitation of the CAP Theorem by addressing system behavior during normal operation, not just during failures.

---

## How DNS Works: A Guide to Understanding the Internet's Address Book

*Added: 2026-08-08 01:40*

**Source:** [https://www.freecodecamp.org/news/how-dns-works-the-internets-address-book/](https://www.freecodecamp.org/news/how-dns-works-the-internets-address-book/)

## Overview
The Domain Name System (DNS) is the internet's address book, translating human-readable domain names like `example.com` into numerical IP addresses that computers use to locate websites and services. This process ensures seamless navigation across the internet.

## The DNS Resolution Process
When you access a domain name, your device first checks its local caches (application and operating system) for the corresponding IP address. If not found, it forwards the request to a configured DNS server, often provided by your internet service provider or a public DNS service. This initial server then begins a recursive search across the global DNS hierarchy.

## The DNS Hierarchy and Recursive Resolution
The recursive resolver, a key component of a DNS server, orchestrates the lookup by interacting with a series of specialized servers:
*   **Root Name Servers:** These are the top of the hierarchy, directing the resolver to the correct Top-Level Domain (TLD) server (e.g., for `.com` or `.org`). There are 13 root server clusters globally, using anycast routing for efficiency and reliability.
*   **TLD Name Servers:** These servers manage specific TLDs and provide the resolver with the address of the authoritative name server for the requested domain.
*   **Authoritative Name Servers:** These servers hold the definitive DNS records (like A, CNAME, MX records) for a particular domain and provide the final IP address to the recursive resolver.
Throughout this process, caching is extensively used at various levels to speed up future queries.

## Domain Registrars and New Domain Setup
Domain registrars are entities that allow individuals and organizations to register and manage domain names. When a new domain is purchased, the registrar registers it with the appropriate registry, configures its name servers, and sets up the DNS zone file with records linking the domain to its hosting server. These changes then propagate across the global DNS network, making the domain accessible.

---
