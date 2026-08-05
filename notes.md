# System Design & Tech Notes

> Auto-generated summaries from articles. Last updated: 2026-08-06.

## Table of Contents

<!-- INDEX START -->
- [Latency, Throughput And Availability](#latency-throughput-and-availability) — *2026-08-06 01:28*
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
