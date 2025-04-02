'use strict';

const express = require('express');
// const morgan = require('morgan'); // logging middleware
const { check, validationResult } = require('express-validator'); // validation middleware
const insegnamentiDao = require('./insegnamenti-dao'); // module for accessing the exams in the DB
// const passport = require('passport'); // auth middleware
// const LocalStrategy = require('passport-local').Strategy; // username and password for login
// const session = require('express-session'); // enable sessions
// const userDao = require('./user-dao'); // module for accessing the users in the DB

/*** Set up Passport ***/
// set up the "username and password" login strategy
// by setting a function to verify username and password
// passport.use(new LocalStrategy(
//   function(username, password, done) {
//     userDao.getUser(username, password).then((user) => {
//       if (!user)
//         return done(null, false, { message: 'Incorrect username and/or password.' });

//       return done(null, user);
//     })
//   }
// ));

// // serialize and de-serialize the user (user object <-> session)
// // we serialize the user id and we store it in the session: the session is very small in this way
// passport.serializeUser((user, done) => {
//   done(null, user.id);
// });

// // starting from the data in the session, we extract the current (logged-in) user
// passport.deserializeUser((id, done) => {
//   userDao.getUserById(id)
//     .then(user => {
//       done(null, user); // this will be available in req.user
//     }).catch(err => {
//       done(err, null);
//     });
// });

// init express
const app = express();
const port = 3001;

// set-up the middlewares
// app.use(morgan('dev'));
app.use(express.json());

// // custom middleware: check if a given request is coming from an authenticated user
// const isLoggedIn = (req, res, next) => {
//   if(req.isAuthenticated())
//     return next();

//   return res.status(401).json({ error: 'not authenticated'});
// }

// // set up the session
// app.use(session({
//   // by default, Passport uses a MemoryStore to keep track of the sessions
//   secret: 'a secret sentence not to share with anybody and anywhere, used to sign the session ID cookie',
//   resave: false,
//   saveUninitialized: false 
// }));

// // then, init passport
// app.use(passport.initialize());
// app.use(passport.session());


/*** Courses/Exams APIs ***/

// GET /api/insegnamenti
app.get('/api/insegnamenti', (req, res) => {
  insegnamentiDao.get_Insegnamenti()
    .then(insegnamenti => res.json(insegnamenti))
    .catch(() => res.status(500).end());
});

// GET /api/pianoAllocazione
app.get('/api/pianoAllocazione', (req, res) => {
  insegnamentiDao.get_PianoAllocazione()
    .then(pianiAllocazione => res.json(pianiAllocazione))
    .catch(() => res.status(500).end());
});

// GET /api/fasceOrarie
app.get('/api/fasceOrarie', (req, res) => {
  insegnamentiDao.get_fasceOrarie()
    .then(fasce => res.json(fasce))
    .catch(() => res.status(500).end());
})

// GET /api/giorni
app.get('/api/giorni', (req, res) => {
  insegnamentiDao.get_giorni()
    .then(giorni => res.json(giorni))
    .catch(() => res.status(500).end());
})

// GET /api/docenti
app.get('/api/docenti', (req, res) => {
  insegnamentiDao.get_docenti()
    .then(docs => res.json(docs))
    .catch(() => res.status(500).end());
})

// GET /api/sovrapposizioni
app.get('/api/sovrapposizioni', (req, res) => {
  insegnamentiDao.get_Info_Correlazioni()
    .then(listInfoCorr => res.json(listInfoCorr))
    .catch(() => res.status(500).end());
})

// GET /api/pianoAllocazione/:pianoAllocazione/:ID_INC
// app.get('/api/pianoAllocazione/:pianoAllocazione/:ID_INC', (req, res) => {
//   insegnamentiDao.get_pianoAllocazioneID_INC_withDocenti(req.params.pianoAllocazione, req.params.ID_INC)
//     .then(slots => res.json(slots))
//     .catch(() => res.status(500).end());
// });

// GET /api/pianoAllocazione/:pianoAllocazione
app.get('/api/pianoAllocazione/:pianoAllocazione', (req, res) => {
  insegnamentiDao.get_slots_pianoAllocazione(req.params.pianoAllocazione)
    .then(slots => res.json(slots))
    .catch(() => res.status(500).end());
})

// GET /api/pianoAllocazione/:pianoAllocazione/:tipoCdl/:nomeCdl/:orientamento
app.get('/api/pianoAllocazione/:pianoAllocazione/:tipoCdl/:nomeCdl/:orientamento/:periodoDidattico', (req, res) => {
  insegnamentiDao.get_pianoAllocazioneOrientamento_withDocenti(req.params.pianoAllocazione, req.params.tipoCdl, req.params.nomeCdl,
    req.params.orientamento, req.params.periodoDidattico)
    .then(slots => res.json(slots))
    .catch(() => res.status(500).end());
})

// GET /api/pianoAllocazione/:pianoAllocazione/:docente
app.get('/api/pianoAllocazione/:pianoAllocazione/:docente', (req, res) => {
  insegnamentiDao.get_pianoAllocazioneDocente(req.params.pianoAllocazione, req.params.docente)
    .then(slots => res.json(slots))
    .catch(() => res.status(500).end());
})

// GET /api/corsiDiLaurea
app.get('/api/corsiDiLaurea', (req, res) => {
  insegnamentiDao.get_corsiDiLaurea()
    .then(cdls => res.json(cdls))
    .catch(() => res.status(500).end());
})

// GET /api/corsiDiLaurea/:tipoCdl
app.get('/api/corsiDiLaurea/:tipoCdl', (req, res) => {
  insegnamentiDao.get_corsiDiLaurea_withTipoCdl(req.params.tipoCdl)
    .then(cdls => res.json(cdls))
    .catch(() => res.status(500).end());
})

// GET /api/orientamenti
app.get('/api/orientamenti', (req, res) => {
  insegnamentiDao.get_Orientamenti()
    .then(orients => res.json(orients))
    .catch(() => res.status(500).end());
})

// GET /api/orientamenti/:tipoCdl/:nomeCdl
app.get('/api/orientamenti/:tipoCdl/:nomeCdl', (req, res) => {
  insegnamentiDao.get_Orientamenti_Cdl(req.params.nomeCdl, req.params.tipoCdl)
    .then(orients => res.json(orients))
    .catch(() => res.status(500).end());
})

// GET /api/insegnamenti/:tipoCdl/:nomeCdl/:orientamento
app.get('/api/insegnamenti/:tipoCdl/:nomeCdl/:orientamento', (req, res) => {
  insegnamentiDao.get_Insegnamenti_withOrientamento(req.params.orientamento, req.params.nomeCdl, req.params.tipoCdl)
    .then(listIns => res.json(listIns))
    .catch(() => res.status(500).end());
})



// // GET /api/courses/<code>
// app.get('/api/courses/:code', async (req, res) => {
//   try {
//     const result = await examDao.getCourse(req.params.code);
//     if(result.error)
//       res.status(404).json(result);
//     else
//       res.json(result);
//   } catch(err) {
//     res.status(500).end();
//   }
// });

// // GET /api/exams
// app.get('/api/exams', isLoggedIn, async (req, res) => {
//   try {
//     const exams = await examDao.listExams(req.user.id);
//     res.json(exams);
//   } catch(err) {
//     res.status(500).end();
//   }
// });

// // POST /api/exams
// app.post('/api/exams', isLoggedIn, [
//   check('score').isInt({min: 18, max: 31}),
//   check('code').isLength({min: 7, max: 7}),
//   check('date').isDate({format: 'YYYY-MM-DD', strictMode: true})
// ], async (req, res) => {
//   const errors = validationResult(req);
//   if (!errors.isEmpty()) {
//     return res.status(422).json({errors: errors.array()});
//   }

//   const exam = {
//     code: req.body.code,
//     score: req.body.score,
//     date: req.body.date,
//   };

//   try {
//     await examDao.createExam(exam, req.user.id);
//     res.status(201).end();
//   } catch(err) {
//     res.status(503).json({error: `Database error during the creation of exam ${exam.code}.`});
//   }
// });

// // PUT /api/exams/<code>
// app.put('/api/exams/:code', isLoggedIn, [
//   check('score').isInt({min: 18, max: 31}),
//   check('code').isLength({min: 7, max: 7}),
//   check('date').isDate({format: 'YYYY-MM-DD', strictMode: true})
// ], async (req, res) => {
//   const errors = validationResult(req);
//   if (!errors.isEmpty()) {
//     return res.status(422).json({errors: errors.array()});
//   }

//   const exam = req.body;

//   // you can also check here if the code passed in the URL matches with the code in req.body
//   try {
//     await examDao.updateExam(exam, req.user.id);
//     res.status(200).end();
//   } catch(err) {
//     res.status(503).json({error: `Database error during the update of exam ${req.params.code}.`});
//   }

// });

// // DELETE /api/exams/<code>
// app.delete('/api/exams/:code', isLoggedIn, async (req, res) => {
//   try {
//     await examDao.deleteExam(req.params.code, req.user.id);
//     res.status(204).end();
//   } catch(err) {
//     res.status(503).json({ error: `Database error during the deletion of exam ${req.params.code}.`});
//   }
// });

// /*** Users APIs ***/

// // POST /sessions 
// // login
// app.post('/api/sessions', function(req, res, next) {
//   passport.authenticate('local', (err, user, info) => {
//     if (err)
//       return next(err);
//       if (!user) {
//         // display wrong login messages
//         return res.status(401).json(info);
//       }
//       // success, perform the login
//       req.login(user, (err) => {
//         if (err)
//           return next(err);

//         // req.user contains the authenticated user, we send all the user info back
//         // this is coming from userDao.getUser()
//         return res.json(req.user);
//       });
//   })(req, res, next);
// });

// // ALTERNATIVE: if we are not interested in sending error messages...
// /*
// app.post('/api/sessions', passport.authenticate('local'), (req,res) => {
//   // If this function gets called, authentication was successful.
//   // `req.user` contains the authenticated user.
//   res.json(req.user);
// });
// */

// // DELETE /sessions/current 
// // logout
// app.delete('/api/sessions/current', (req, res) => {
//   req.logout();
//   res.end();
// });

// // GET /sessions/current
// // check whether the user is logged in or not
// app.get('/api/sessions/current', (req, res) => {
//   if(req.isAuthenticated()) {
//     res.status(200).json(req.user);}
//   else
//     res.status(401).json({error: 'Unauthenticated user!'});;
// });

/*** Other express-related instructions ***/

// Activate the server
app.listen(port, () => {
  console.log(`react-score-server listening at http://localhost:${port}`);
});