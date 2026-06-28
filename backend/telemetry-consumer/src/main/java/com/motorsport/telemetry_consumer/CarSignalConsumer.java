package com.motorsport.telemetry_consumer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class CarSignalConsumer {

    @Autowired
    private CarSignalRepository carSignalRepository;

    @KafkaListener(topics = "car.signals.raw", groupId = "telemetry-consumer-group")
    public void consume(CarSignal signal) {
        carSignalRepository.save(signal);
        System.out.println("Saved signal for lap: " + signal.getLapId());
    }
}