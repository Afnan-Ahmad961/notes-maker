# System Design & Tech Notes

> Auto-generated summaries from articles. Last updated: 2026-08-06.

## Table of Contents

<!-- INDEX START -->
- [Latency, Throughput And Availability](#latency-throughput-and-availability) — *2026-08-06 01:28*
- [Horizontal and Vertical Scaling | System Design](#horizontal-and-vertical-scaling-system-design) — *2026-08-06 01:44*
- [Describe the CAP theorem and its implications for distributed systems](#describe-the-cap-theorem-and-its-implications-for-distributed-systems) — *2026-08-07 19:41*
- [PACELC Theorem](#pacelc-theorem) — *2026-08-08 00:23*
- [How DNS Works: A Guide to Understanding the Internet's Address Book](#how-dns-works-a-guide-to-understanding-the-internets-address-book) — *2026-08-08 01:40*
- [Content Distribution Network (CDN)](#content-distribution-network-cdn) — *2026-08-08 01:57*
- [Load Balancing Strategies: Round-Robin, Least Connections, and Consistent Hashing](#load-balancing-strategies-round-robin-least-connections-and-consistent-hashing) — *2026-08-08 19:49*
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

## Content Distribution Network (CDN)

*Added: 2026-08-08 01:57*

**Source:** [https://www.geeksforgeeks.org/computer-networks/what-is-a-content-distribution-network-and-how-does-it-work/](https://www.geeksforgeeks.org/computer-networks/what-is-a-content-distribution-network-and-how-does-it-work/)

## Overview
A Content Distribution Network (CDN) is a system of geographically distributed servers designed to deliver web content to users more quickly and efficiently. By storing copies of content closer to users, CDNs reduce the physical distance data travels, leading to faster load times, lower latency, and improved website performance.

## Key Components
A CDN operates through several core elements. The **Origin Server** is where the original content is hosted. **Points of Presence (PoPs)** are physical data centers located in various regions or cities. Within each PoP, **Edge Servers** directly serve user requests, holding a **Cache** of frequently accessed content. The **CDN DNS / Request Routing** system directs users to the nearest and most optimal edge server.

## How a CDN Works
When a user requests content, the CDN's DNS system routes the request to an edge server in a PoP geographically closest to the user. If the content is cached on that edge server, it's delivered immediately. If not, the edge server fetches the content from the origin server, serves it to the user, and then caches it for future requests. This process significantly shortens the data path, reducing latency and speeding up delivery.

## Advantages
CDNs offer numerous benefits, including **faster load times** and **lower latency** due to content being served from nearby locations. They **reduce the load on origin servers** by offloading traffic to edge servers and **increase availability** by distributing requests across multiple points. CDNs are also effective at **handling traffic spikes** and can lead to **lower bandwidth costs** for content providers, ultimately providing a **better user experience**.

## Limitations
Despite their advantages, CDNs have some drawbacks. They introduce **extra costs** for services. There can be challenges with **cache inconsistency**, where users might see outdated content if not managed properly. Debugging issues can be harder due to **less control at the edge**. CDNs may also be less effective for **highly dynamic content** and can have **regional gaps** in coverage. Incorrect configuration can also pose **security risks**.

## Applications
CDNs are widely used across various industries. They are crucial for **video streaming** services to ensure smooth playback and less buffering. They accelerate **website performance** by quickly delivering static assets like images and scripts. CDNs also facilitate faster **software and application downloads**, improve **gaming** experiences by speeding up updates, and enhance **e-commerce** sites by handling peak traffic. They can also improve **API response times** and provide **security at the edge** by mitigating DDoS attacks.

---

## Load Balancing Strategies: Round-Robin, Least Connections, and Consistent Hashing

*Added: 2026-08-08 19:49*

## Overview

Load balancers are critical components in modern distributed systems, ensuring efficient distribution of incoming network traffic across multiple servers. This article explains how load balancers enable horizontal scaling and improve system reliability by choosing the right algorithm to direct requests. It differentiates between Layer 4 and Layer 7 load balancing and details several common algorithms, highlighting their strengths and ideal use cases.

## The Role of Load Balancers

Load balancers distribute incoming client requests among available server instances, preventing any single server from becoming overloaded and ensuring optimal resource utilization. They are essential for scaling applications horizontally, improving performance, and maintaining high availability by directing traffic away from unhealthy instances. The choice of load balancing algorithm significantly impacts how evenly load is spread and how the system behaves under various conditions.

## Layer 4 vs. Layer 7 Balancing

Load balancers operate at different layers of the network stack, influencing their capabilities:

*   **Layer 4 (Transport Layer):** Routes traffic based on basic network information like IP addresses and TCP/UDP ports. It's fast and efficient because it doesn't inspect the content of the request.
*   **Layer 7 (Application Layer):** Inspects the full request content, including HTTP headers, URLs, and cookies. This allows for more intelligent routing decisions based on application-specific logic, making it common for microservices.

## Common Load Balancing Algorithms

Different algorithms are suited for different workloads and system requirements:

### Round-Robin

This is the simplest method, distributing requests sequentially to each server in the pool. It ensures an even distribution of request *counts*. A "weighted" version can be used to send more requests to servers with higher capacity. It works best for stateless services where requests are similar in processing cost.

### Least Connections

This algorithm directs new requests to the server with the fewest active connections. It is more adaptive than round-robin because it considers the actual load on servers, accounting for varying request durations. A "weighted" version can also be applied for servers with different capacities.

### Least Response Time

An advanced variant of least connections, this algorithm routes requests to the server with the fewest active connections and the lowest average response time. It helps to avoid temporarily slow instances, providing more precise load distribution.

### IP Hash

With IP hash, the client's IP address is used to determine which server handles the request. This ensures that requests from the same client consistently go to the same server, which is useful for maintaining session affinity without requiring the load balancer to track session state.

---
