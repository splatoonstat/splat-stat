create table if not exists battles (
    season varchar(31),
    period timestamp,
    date date,
    "game-ver" varchar(15),
    lobby varchar(31),
    mode varchar(31),
    stage varchar(31),
    time integer,
    win varchar(15),
    knockout boolean,
    rank varchar(15),
    power decimal,
    "alpha-inked" integer,
    "alpha-ink-percent" decimal,
    "alpha-count" integer,
    "alpha-color" varchar(15),
    "alpha-theme" varchar(255),
    "bravo-inked" integer,
    "bravo-ink-percent" decimal,
    "bravo-count" integer,
    "bravo-color" varchar(15),
    "bravo-theme" varchar(255),
    "A1-weapon" varchar(31),
    "A1-kill-assist" integer,
    "A1-kill" integer,
    "A1-assist" integer,
    "A1-death" integer,
    "A1-special" integer,
    "A1-inked" integer,
    "A1-abilities" varchar(511),
    "A2-weapon" varchar(31),
    "A2-kill-assist" integer,
    "A2-kill" integer,
    "A2-assist" integer,
    "A2-death" integer,
    "A2-special" integer,
    "A2-inked" integer,
    "A2-abilities" varchar(511),
    "A3-weapon" varchar(31),
    "A3-kill-assist" integer,
    "A3-kill" integer,
    "A3-assist" integer,
    "A3-death" integer,
    "A3-special" integer,
    "A3-inked" integer,
    "A3-abilities" varchar(511),
    "A4-weapon" varchar(31),
    "A4-kill-assist" integer,
    "A4-kill" integer,
    "A4-assist" integer,
    "A4-death" integer,
    "A4-special" integer,
    "A4-inked" integer,
    "A4-abilities" varchar(511),
    "B1-weapon" varchar(31),
    "B1-kill-assist" integer,
    "B1-kill" integer,
    "B1-assist" integer,
    "B1-death" integer,
    "B1-special" integer,
    "B1-inked" integer,
    "B1-abilities" varchar(511),
    "B2-weapon" varchar(31),
    "B2-kill-assist" integer,
    "B2-kill" integer,
    "B2-assist" integer,
    "B2-death" integer,
    "B2-special" integer,
    "B2-inked" integer,
    "B2-abilities" varchar(511),
    "B3-weapon" varchar(31),
    "B3-kill-assist" integer,
    "B3-kill" integer,
    "B3-assist" integer,
    "B3-death" integer,
    "B3-special" integer,
    "B3-inked" integer,
    "B3-abilities" varchar(511),
    "B4-weapon" varchar(31),
    "B4-kill-assist" integer,
    "B4-kill" integer,
    "B4-assist" integer,
    "B4-death" integer,
    "B4-special" integer,
    "B4-inked" integer,
    "B4-abilities" varchar(511),
    "medal1-grade" varchar(15),
    "medal1-name" varchar(255),
    "medal2-grade" varchar(15),
    "medal2-name" varchar(255),
    "medal3-grade" varchar(15),
    "medal3-name" varchar(255)
);
