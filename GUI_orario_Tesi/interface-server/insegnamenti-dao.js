'use strict';
/* Data Access Object (DAO) module for accessing db. 
THE APIs have the same names as Python APIs, see dbAPI.py for the documentation */

const db = require('./db');

// Returns all the possible time slots
exports.get_fasceOrarie = () => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT DISTINCT fasciaOraria FROM SlotSettimana';
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listFasce = rows.map((fascia) => ({
                fasciaOraria: fascia.fasciaOraria
            }));
            resolve(listFasce);
        })
    })
}

exports.get_Info_Correlazioni = () => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT * FROM Info_correlazioni';
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listInfoCorr = rows.map((infoCorr) => ({
                ID_INC_1: infoCorr.ID_INC_1, ID_INC_2: infoCorr.ID_INC_2, correlazione: infoCorr.Correlazione_finale !== null ? infoCorr.Correlazione_finale : infoCorr.Correlazione
            }));
            resolve(listInfoCorr);
        })
    })
}

exports.get_giorni = () => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT DISTINCT giorno FROM SlotSettimana ORDER BY giorno ASC';
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listGiorni = rows.map((g) => ({
                giorno: g.giorno
            }));
            resolve(listGiorni);
        })
    })
}

exports.get_docenti = () => {
    return new Promise((resolve, reject) => {
        // Not sure about Docente (Teacher) correctness
        const sql = 'SELECT DISTINCT Cognome FROM Docente_in_Slot';
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listDoc = rows.map((doc) => ({
                Cognome: doc.Cognome
            }));
            resolve(listDoc);
        })
    })
}

exports.get_Insegnamenti = () => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT * FROM Insegnamento';
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listIns = rows.map((ins) => ({
                ID_INC: ins.ID_INC, nStudenti: ins.nStudenti, nStudentiFreq: ins.nStudentiFreq, collegio: ins.collegio, titolo: ins.titolo,
                CFU: ins.CFU, oreLez: ins.oreLez, titolare: ins.titolare
            }));
            resolve(listIns);
        });
    });
}

exports.get_PianoAllocazione = () => {
    return new Promise((resolve, reject) => {
        const sql = 'SELECT * FROM PianoAllocazione'
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listPiani = rows.map((piano) => ({
                pianoAllocazione: piano.pianoAllocazione
            }));
            resolve(listPiani);
        })
    })
}

exports.get_Insegnamenti_withOrientamento = (orientamento, nomeCdl, tipoCdl) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT I.ID_INC, I.nStudenti, I.nStudentiFreq, I.collegio, \
        I.titolo, I.CFU, I.oreLez, I.titolare, IiO.nStudenti AS nStudentiOrient, IiO.tipoInsegnamento, IiO.periodoDidattico, IiO.alfabetica \
                    FROM Insegnamento_in_Orientamento IiO, Insegnamento I \
                    WHERE IiO.ID_INC = I.ID_INC AND IiO.orientamento = ? AND IiO.nomeCdl = ? AND Iio.tipoCdl = ?";
        db.all(sql, [orientamento, nomeCdl, tipoCdl], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listIns = rows.map((ins) => ({
                ID_INC: ins.ID_INC, nStudenti: ins.nStudenti, nStudentiFreq: ins.nStudentiFreq, collegio: ins.collegio, titolo: ins.titolo,
                CFU: ins.CFU, oreLez: ins.oreLez, titolare: ins.titolare, nStudentiOrient: ins.nStudentiOrient,
                tipoInsegnamento: ins.tipoInsegnamento, periodoDidattico: ins.periodoDidattico, alfabetica: ins.alfabetica
            }));
            resolve(listIns);
        })
    })
}

exports.get_pianoAllocazioneID_INC_withDocenti = (pianoAllocazione, ID_INC) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * \
                    FROM Slot S, Docente_in_Slot DiS \
                    WHERE S.pianoAllocazione = ? AND S.ID_INC = ? AND S.idSlot = DiS.idSlot AND S.pianoAllocazione = DiS.pianoAllocazione \
                    ORDER BY S.idSlot";
        db.all(sql, [pianoAllocazione, ID_INC], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const slots = rows.map((slot) => ({
                pianoAllocazione: slot.pianoAllocazione, idSlot: slot.idSlot, nStudentiAssegnati: slot.nStudentiAssegnati,
                tipoLez: slot.tipoLez, numSlotConsecutivi: slot.numSlotConsecutivi, ID_INC: slot.ID_INC, giorno: slot.giorno,
                fasciaOraria: slot.fasciaOraria, tipoLocale: slot.tipoLocale, tipoErogazione: slot.tipoErogazione, Cognome: slot.Cognome
            }));
            resolve(slots);
        })
    })
}

exports.get_slots_pianoAllocazione = (pianoAllocazione) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * \
                    FROM Slot S, Docente_in_Slot DiS, Insegnamento I, Insegnamento_in_Orientamento IiO \
                    WHERE S.idSlot = DiS.idSlot AND S.pianoAllocazione = DiS.pianoAllocazione AND I.ID_INC = S.ID_INC AND IiO.ID_INC = I.ID_INC\
                    AND S.pianoAllocazione = ? \
                    ORDER BY S.idSlot";
        db.all(sql, [pianoAllocazione], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const slots = rows.map((slot) => ({
                pianoAllocazione: slot.pianoAllocazione, idSlot: slot.idSlot, nStudentiAssegnati: slot.nStudentiAssegnati,
                tipoLez: slot.tipoLez, numSlotConsecutivi: slot.numSlotConsecutivi, ID_INC: slot.ID_INC, giorno: slot.giorno,
                fasciaOraria: slot.fasciaOraria, tipoLocale: slot.tipoLocale, tipoErogazione: slot.tipoErogazione, Cognome: slot.Cognome,
                tipoInsegnamento: slot.tipoInsegnamento,
                // per assegnare anche l'Insegnamento
                nStudenti: slot.nStudenti, nStudentiFreq: slot.nStudentiFreq, collegio: slot.collegio, titolo: slot.titolo, CFU: slot.CFU,
                oreLez: slot.oreLez, titolare: slot.titolare, nStudentiOrient: slot.nStudentiOrient, alfabetica: slot.alfabetica
            }));
            resolve(slots);
        })
    })
}

exports.get_pianoAllocazioneOrientamento_withDocenti = (pianoAllocazione, tipoCdl, nomeCdl, orientamento, periodoDidattico) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * \
                    FROM Slot S, Docente_in_Slot DiS, Insegnamento I, Insegnamento_in_Orientamento IiO \
                    WHERE S.idSlot = DiS.idSlot AND S.pianoAllocazione = DiS.pianoAllocazione AND I.ID_INC = S.ID_INC AND IiO.ID_INC = I.ID_INC \
                    AND S.pianoAllocazione = ? AND IiO.periodoDidattico = ? AND IiO.orientamento = ? AND IiO.nomeCdl = ? AND IiO.tipoCdl = ? \
                    ORDER BY S.idSlot";
        db.all(sql, [pianoAllocazione, periodoDidattico, orientamento, nomeCdl, tipoCdl], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const slots = rows.map((slot) => ({
                pianoAllocazione: slot.pianoAllocazione, idSlot: slot.idSlot, nStudentiAssegnati: slot.nStudentiAssegnati,
                tipoLez: slot.tipoLez, numSlotConsecutivi: slot.numSlotConsecutivi, ID_INC: slot.ID_INC, giorno: slot.giorno,
                fasciaOraria: slot.fasciaOraria, tipoLocale: slot.tipoLocale, tipoErogazione: slot.tipoErogazione, Cognome: slot.Cognome,
                tipoInsegnamento: slot.tipoInsegnamento,
                // per assegnare anche l'Insegnamento
                nStudenti: slot.nStudenti, nStudentiFreq: slot.nStudentiFreq, collegio: slot.collegio, titolo: slot.titolo, CFU: slot.CFU,
                oreLez: slot.oreLez, titolare: slot.titolare, nStudentiOrient: slot.nStudentiOrient, alfabetica: slot.alfabetica
            }));
            resolve(slots);
        })
    })
}

exports.get_otherTimetable = (tipoCdl, nomeCdl, orientamento, periodoDidattico) => {
    const days = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
    const time_slots = ["8.30-10.00", "10.00-11.30", "11.30-13.00", "13.00-14.30", "14.30-16.00", "16.00-17.30", "17.30-19.00"]
    return new Promise((resolve, reject) => {
        const sql = "SELECT PS.ID_INC, lectureType, day, timeSlot, lectGroup, I.titolo, IiO.alfabetica \
                    FROM PreviousSolution PS, Insegnamento I, Insegnamento_in_Orientamento IiO \
                    WHERE I.ID_INC = PS.ID_INC AND IiO.ID_INC = I.ID_INC \
                    AND IiO.periodoDidattico = ? AND IiO.orientamento = ? AND IiO.nomeCdl = ? AND IiO.tipoCdl = ?";
        db.all(sql, [periodoDidattico, orientamento, nomeCdl, tipoCdl], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const slots = rows.map((slot) => ({
                idSlot: slot.ID_INC + "_" + (slot.lectureType == "L" ? "" : (slot.lectureType == "EA" ? "practice_group" : "lab_group")) + (slot.lectureType != "L" ? (slot.lectGroup == "No squadra" ? "1" : slot.lectGroup.substr(slot.lectGroup.length - 1)) : "") + "_slot_" + (7*days.indexOf(slot.day) + time_slots.indexOf(slot.timeSlot)),
                tipoLez: slot.lectureType, ID_INC: slot.ID_INC, giorno: slot.day,
                fasciaOraria: slot.timeSlot, numSlotConsecutivi: 1, tipoLocale: "Aula",
                tipoInsegnamento: "Obbligatorio", titolo: slot.titolo, alfabetica: slot.alfabetica
            }));
            resolve(slots);
        })
    })
}

exports.get_pianoAllocazioneDocente = (pianoAllocazione, docente) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT S.pianoAllocazione, S.idSlot, S.nStudentiAssegnati, S.tipoLez, S.numSlotConsecutivi, S.ID_INC, S.giorno, \
                        S.fasciaOraria, S.tipoLocale, S.tipoErogazione, DiS.Cognome, I.nStudenti, I.nStudentiFreq, I.collegio, I.titolo, \
                        I.CFU, I.oreLez, I.titolare \
                    FROM Docente_in_Slot DiS, Slot S, Insegnamento I \
                    WHERE S.idSlot = DiS.idSlot AND S.pianoAllocazione = DiS.pianoAllocazione AND I.ID_INC = S.ID_INC \
                    AND S.pianoAllocazione = ? AND DiS.Cognome = ? \
                    ORDER BY S.idSlot";
        db.all(sql, [pianoAllocazione, docente], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const slots = rows.map((slot) => ({
                pianoAllocazione: slot.pianoAllocazione, idSlot: slot.idSlot, nStudentiAssegnati: slot.nStudentiAssegnati,
                tipoLez: slot.tipoLez, numSlotConsecutivi: slot.numSlotConsecutivi, ID_INC: slot.ID_INC, giorno: slot.giorno,
                fasciaOraria: slot.fasciaOraria, tipoLocale: slot.tipoLocale, tipoErogazione: slot.tipoErogazione, Cognome: slot.Cognome,
                // Teaching
                nStudenti: slot.nStudenti, nStudentiFreq: slot.nStudentiFreq, collegio: slot.collegio, titolo: slot.titolo, CFU: slot.CFU,
                oreLez: slot.oreLez, titolare: slot.titolare
            }));

            resolve(slots);
        })
    })
}

exports.get_corsiDiLaurea_withTipoCdl = (tipoCdl) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * FROM Corso_di_laurea WHERE tipoCdl = ?";
        db.all(sql, [tipoCdl], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listCdl = rows.map((cdl) => ({
                tipoCdl: cdl.tipoCdl, nomeCdl: cdl.nomeCdl
            }));
            resolve(listCdl);
        })
    })
}

exports.get_corsiDiLaurea = () => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * FROM Corso_di_laurea";
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listCdl = rows.map((cdl) => ({
                tipoCdl: cdl.tipoCdl, nomeCdl: cdl.nomeCdl
            }));
            resolve(listCdl);
        })
    })
}

exports.get_Orientamenti = () => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * FROM Orientamento";
        db.all(sql, [], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listOrient = rows.map((orient) => ({
                orientamento: orient.orientamento, nomeCdl: orient.nomeCdl, tipoCdl: orient.tipoCdl
            }));
            resolve(listOrient);
        })
    })
}

exports.get_Orientamenti_Cdl = (nomeCdl, tipoCdl) => {
    return new Promise((resolve, reject) => {
        const sql = "SELECT * FROM Orientamento WHERE nomeCdl = ? AND tipoCdl = ?";
        db.all(sql, [nomeCdl, tipoCdl], (err, rows) => {
            if (err) {
                reject(err);
                return;
            }
            const listOrient = rows.map((orient) => ({
                orientamento: orient.orientamento, nomeCdl: orient.nomeCdl, tipoCdl: orient.tipoCdl
            }));
            resolve(listOrient);
        })
    })
}

