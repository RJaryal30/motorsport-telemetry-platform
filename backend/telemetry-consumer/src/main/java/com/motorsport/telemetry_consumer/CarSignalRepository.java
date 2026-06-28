package com.motorsport.telemetry_consumer;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CarSignalRepository extends JpaRepository<CarSignal, Long> {
}