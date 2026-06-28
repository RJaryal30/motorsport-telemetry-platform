package com.motorsport.telemetry_consumer;

import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "car_signals")
public class CarSignal {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @JsonProperty("lap_id")
    @Column(name = "lap_id")
    private UUID lapId;

    @JsonProperty("session_time_ms")
    @Column(name = "session_time_ms")
    private Long sessionTimeMs;

    private Integer speed;
    private Integer rpm;
    private Integer throttle;
    private Boolean brake;
    private Integer gear;
    private Integer drs;

    // JPA requires a no-argument constructor
    public CarSignal() {
    }

    // Getters and setters - JPA and Jackson (JSON deserialization) both need these
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public UUID getLapId() {
        return lapId;
    }

    public void setLapId(UUID lapId) {
        this.lapId = lapId;
    }

    public Long getSessionTimeMs() {
        return sessionTimeMs;
    }

    public void setSessionTimeMs(Long sessionTimeMs) {
        this.sessionTimeMs = sessionTimeMs;
    }

    public Integer getSpeed() {
        return speed;
    }

    public void setSpeed(Integer speed) {
        this.speed = speed;
    }

    public Integer getRpm() {
        return rpm;
    }

    public void setRpm(Integer rpm) {
        this.rpm = rpm;
    }

    public Integer getThrottle() {
        return throttle;
    }

    public void setThrottle(Integer throttle) {
        this.throttle = throttle;
    }

    public Boolean getBrake() {
        return brake;
    }

    public void setBrake(Boolean brake) {
        this.brake = brake;
    }

    public Integer getGear() {
        return gear;
    }

    public void setGear(Integer gear) {
        this.gear = gear;
    }

    public Integer getDrs() {
        return drs;
    }

    public void setDrs(Integer drs) {
        this.drs = drs;
    }
}