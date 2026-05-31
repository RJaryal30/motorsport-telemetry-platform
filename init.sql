CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    year            SMALLINT NOT NULL,
    gp_name         VARCHAR(100) NOT NULL,
    session_type    VARCHAR(20) NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE laps (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id          UUID REFERENCES sessions(id),
    driver_code         CHAR(3) NOT NULL,
    team                VARCHAR(50),
    lap_number          SMALLINT NOT NULL,
    lap_time_ms         INTEGER,
    sector1_ms          INTEGER,
    sector2_ms          INTEGER,
    sector3_ms          INTEGER,
    compound            VARCHAR(10),
    tyre_life           SMALLINT,
    stint               SMALLINT,
    fresh_tyre          BOOLEAN,
    position            SMALLINT,
    track_status        VARCHAR(10),
    pit_in_time_ms      BIGINT,
    pit_out_time_ms     BIGINT,
    is_personal_best    BOOLEAN DEFAULT FALSE,
    deleted             BOOLEAN DEFAULT FALSE,
    deleted_reason      VARCHAR(50),
    is_accurate         BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_laps_session_driver ON laps(session_id, driver_code);

CREATE TABLE car_signals (
    id                  BIGSERIAL PRIMARY KEY,
    lap_id              UUID REFERENCES laps(id),
    session_time_ms     BIGINT NOT NULL,
    speed               SMALLINT,
    rpm                 INTEGER,
    throttle            SMALLINT,
    brake               BOOLEAN,
    gear                SMALLINT,
    drs                 SMALLINT
);

CREATE INDEX idx_car_signals_lap ON car_signals(lap_id);

CREATE TABLE race_context (
    id                      BIGSERIAL PRIMARY KEY,
    lap_id                  UUID REFERENCES laps(id),
    session_time_ms         BIGINT NOT NULL,
    x                       FLOAT,
    y                       FLOAT,
    z                       FLOAT,
    distance                FLOAT,
    relative_distance       FLOAT,
    status                  VARCHAR(20),
    driver_ahead            CHAR(3),
    dist_to_driver_ahead    FLOAT
);

CREATE INDEX idx_race_context_lap ON race_context(lap_id);