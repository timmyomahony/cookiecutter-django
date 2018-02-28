let gulp = require('gulp'),
    pjson = require('./package.json'),
    concat = require('gulp-concat'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    postcss = require('gulp-postcss'),
    babel = require('gulp-babel'),
    autoprefixer = require('gulp-autoprefixer'),
    cssnano = require('gulp-cssnano'),
    uglify = require('gulp-uglify'),
    spawn = require('child_process').spawn,
    rename = require('gulp-rename'),
    plumber = require('gulp-plumber'),
    imagemin = require('gulp-imagemin'),
    runSequence = require('run-sequence'),
    browserSync = require('browser-sync').create(),
    reload = browserSync.reload;

let pathsConfig = function (appName) {
    this.app = "./" + (appName || pjson.name);
    return {
        app: this.app,
        templates: `${this.app}/templates`,
        index: `index.html`,
        src: `${this.app}/static/src`,
        build: `${this.app}/static/build`,
    }
};

let paths = pathsConfig();

/**
 * CSS assets
 * 
 * The SASS files are run through postcss/autoprefixer and placed into one 
 * single main styles.min.css file (and sourcemap)
 */
gulp.task('styles', function () {
    let processors = [
        autoprefixer,
        cssnano
    ];
    let styles = gulp.src(`${paths.src}/sass/styles.scss`)
        .pipe(sourcemaps.init())
        .pipe(sass({
            includePaths: [
                'node_modules/'
            ]
        }).on('error', sass.logError))
        .pipe(plumber())
        .pipe(postcss(processors))
        .pipe(rename('styles.min.css'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(`${paths.build}/css/`));
    return [styles];
});

/**
 * Javascript assets
 * 
 * All regular .js files are collected, minified and concatonated into one
 * single main.min.js file (and sourcemap)
 */
gulp.task('scripts', function () {
    return gulp.src([`${paths.src}/js/**/*.js`])
        .pipe(sourcemaps.init())
        .pipe(babel({
            presets: ['es2015']
        }))
        .pipe(plumber())
        .pipe(uglify())
        .pipe(concat('scripts.min.js'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(`${paths.build}/js/`));
});

/**
 * External Javascript assets
 * 
 * Any required external libraries are collected, minified and concatonated 
 * into one single vendor.min.js file (and sourcemap)
 */
gulp.task('vendor', function () {
    return gulp.src([
            'node_modules/jquery/dist/jquery.js',
        ])
        .pipe(concat('vendor.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest(`${paths.build}/js/`));
});

gulp.task('imgCompression', function () {
    return gulp.src(`${paths.src}/images/*`)
        .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
        .pipe(gulp.dest(`${paths.build}/images/`));
});

gulp.task('copy', function () {
    return gulp.src([`${paths.src}/fonts/**/*`], {
            base: `${paths.src}`
        })
        .pipe(gulp.dest(`${paths.build}`));
});

gulp.task('runServer', function (cb) {
    var cmd = spawn('python', ['manage.py', 'runserver_plus'], { stdio: 'inherit' });
    cmd.on('close', function (code) {
        console.log('runServer exited with code ' + code);
        cb(code);
    });
});

gulp.task('browserSync', function () {
    browserSync.init(
        [`${paths.build}/css/.css`, `${paths.build}/js/*.js`, `${paths.templates}/*.html`], {
            // Proxying the django Docker container
            // https://stackoverflow.com/questions/42456424/browsersync-within-a-docker-container
            proxy: "django:8000",
            open: false
        });
});

gulp.task('watch', function () {
    gulp.watch(`${paths.src}/sass/**/*.scss`, ['styles']).on("change", reload);
    gulp.watch(`${paths.src}/js/**/*.js`, ['scripts']).on("change", reload);
    gulp.watch(`${paths.src}/images/**/*`, ['imgCompression']);
    gulp.watch(`${paths.index}`).on("change", reload);
});

gulp.task('default', function () {
    runSequence(
        ['styles', 'scripts', 'vendor', 'imgCompression', 'copy'],
        ['browserSync', 'watch']);
});
