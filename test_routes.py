from page_routes import *


@app.route('/slearning', methods=['GET', 'POST'])
def save_learning():
    if 'loggedin' in session:
        if request.method == 'POST':
            check_naturalist = len(request.form.getlist("check_naturalist"))
            check_intrapersonal = len(request.form.getlist("check_intrapersonal"))
            check_interpersonal = len(request.form.getlist("check_interpersonal"))
            check_musical = len(request.form.getlist("check_musical"))
            check_bodily = len(request.form.getlist("check_bodily"))
            check_spatial = len(request.form.getlist("check_spatial"))
            check_logical = len(request.form.getlist("check_logical"))
            check_linguistic = len(request.form.getlist("check_linguistic"))

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO learning_style VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                session['id'], check_linguistic, check_logical, check_spatial, check_bodily,
                check_musical, check_interpersonal, check_intrapersonal, check_naturalist))
            mysql.connection.commit()

        return redirect(url_for("profile"))

    return redirect(url_for('login'))


@app.route('/sinterest', methods=['GET', 'POST'])
def save_interest():
    if 'loggedin' in session:

        check_realistic = len(request.form.getlist("check_realistic"))
        check_investigate = len(request.form.getlist("check_investigate"))
        check_artistic = len(request.form.getlist("check_artistic"))
        check_social = len(request.form.getlist("check_social"))
        check_enterprising = len(request.form.getlist("check_enterprising"))
        check_conventional = len(request.form.getlist("check_conventional"))

        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO interest VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)', (
                session['id'], check_realistic, check_investigate, check_artistic, check_social, check_enterprising,
                check_conventional))
            mysql.connection.commit()

        return redirect(url_for('profile'))
    return redirect(url_for('login'))


@app.route('/sacademic', methods=['GET', 'POST'])
def save_academic():
    if 'loggedin' in session:
        if request.method == 'POST' and "mathematics" in request.form and "science" in request.form and "english" in request.form and "social_science" in request.form:
            mathematics = request.form.get("mathematics")
            science = request.form.get("science")
            english = request.form.get("english")
            social_science = request.form.get("social_science")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO academic VALUES (NULL, %s, %s, %s, %s, %s)', (
                session['id'], mathematics, science, social_science, english))
            mysql.connection.commit()

        return redirect(url_for("profile"))
    return redirect(url_for('login'))


def transform_to_percentage(test_type, number_of_questions):
    total = 0
    for key in test_type.keys():
        if key != "id" and key != "user_id":
            percentage = round(test_type[key] * 100 / number_of_questions, 2)
            total += percentage
            test_type[key] = percentage
    for key in test_type.keys():
        if key != "id" and key != "user_id":
            percentage = test_type[key]
            if total > 0:
                test_type[key] = f"{round(percentage / total * 100, 2)}%"
            else:
                test_type[key] = "0%"
    if total == 0:
        return True

    return False




@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor, learning_style, academic, interest = get_test_results()
        cursor.execute(f'SELECT * FROM result WHERE user_id={session["id"]} ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        mysql.connection.commit()
        final_result = None
        if result:
            results = [("stem", round(result["stem"] * 100, 2)), ("humss", round(result["humss"] * 100, 2)),
                       ("abm", round(result["abm"] * 100, 2)),
                       ("gas", round(result["gas"] * 100, 2))]
            results.sort(key=lambda x: -x[1])
            final_result = results[0][0]
        first_load = False
        if not learning_style and not academic and not interest:
            first_load = True

        has_missing = False
        is_enough = is_data_enough(learning_style, interest)
        if learning_style:
            has_missing = has_missing or transform_to_percentage(learning_style, 8)
        if interest:
            has_missing = has_missing or transform_to_percentage(interest, 7)
        if not academic:
            has_missing = True
        return render_template('profile.html',
                               username=session['username'],
                               results=final_result,
                               learning_style=learning_style,
                               academic=academic, interest=interest,
                               is_data_enough=is_enough,
                               first_load=first_load,
                               has_missing=has_missing,
                               )
    return redirect(url_for('login'))


"""
This is a helper function that returns the result of each tests
"""


def get_test_results():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        f'SELECT * FROM learning_style WHERE user_id={session["id"]} ORDER BY id DESC LIMIT 1')
    learning_style = cursor.fetchone()
    cursor.execute(f'SELECT * FROM academic WHERE user_id={session["id"]} ORDER BY id DESC LIMIT 1')
    academic = cursor.fetchone()
    cursor.execute(f'SELECT * FROM interest WHERE user_id={session["id"]} ORDER BY id DESC LIMIT 1')
    interest = cursor.fetchone()

    return cursor, learning_style, academic, interest


"""
This is a helper function that transforms result into a single x value
"""


def get_x_value(learning_style, academic, interest):
    x = [interest["result_realistic"], interest["result_investigate"], interest["result_artistic"],
         interest["result_social"], interest["result_enterprising"],
         interest["result_conventional"], learning_style["result_linguistic"], learning_style["result_logical"],
         learning_style["result_spatial"],
         learning_style["result_bodily"], learning_style["result_musical"], learning_style["result_interpersonal"],
         learning_style["result_intrapersonal"], learning_style["result_naturalist"], academic["result_math"],
         academic["result_english"],
         academic["result_science"], academic["result_social_science"]]

    return x


@app.route('/generate')
def generate():
    if 'loggedin' in session:
        cursor, learning_style, academic, interest = get_test_results()

        if not (learning_style and academic and interest):
            return render_template('profile.html', username=session['username'], result=None,
                                   learning_style=learning_style,
                                   academic=academic, interest=interest)

        x = get_x_value(learning_style, academic, interest)

        prob_stem, prob_humss, prob_abm, prob_gas = predict_probabilities([x])[0]

        if academic["result_math"] < 85 or academic["result_science"] < 85:
            prob_stem = 0

        cursor.execute('INSERT INTO result VALUES (NULL, %s, %s, %s, %s, %s)',
                       (session['id'], prob_stem, prob_humss, prob_abm, prob_gas))
        mysql.connection.commit()

        return redirect(url_for('profile'))

    return redirect(url_for('login'))


# Helper functions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


THRESHOLD_NO_FEATURES_LEARNING_STYLE = 6
THRESHOLD_NO_FEATURES_INTEREST = 4
THRESHOLD_NO_CHECKS = 1
THRESHOLD_RELIABLE_CHECKS = 3


def is_data_enough(learning_style, interest):
    if not learning_style or not interest:
        return False

    learning_style_feature_count = 0

    reliable_checks = 0

    for key, checks in learning_style.items():
        if key != "id" and key != "user_id":
            if checks >= THRESHOLD_NO_CHECKS:
                learning_style_feature_count += 1
            if checks >= THRESHOLD_RELIABLE_CHECKS:
                reliable_checks += 1
    if learning_style_feature_count < THRESHOLD_NO_FEATURES_LEARNING_STYLE or reliable_checks == 0:
        return False

    reliable_checks = 0
    interest_feature_count = 0
    for key, checks in learning_style.items():
        if key != "id" and key != "user_id":
            if checks >= THRESHOLD_NO_CHECKS:
                interest_feature_count += 1
            if checks >= THRESHOLD_RELIABLE_CHECKS:
                reliable_checks += 1
    if interest_feature_count < THRESHOLD_NO_FEATURES_INTEREST or reliable_checks == 0:
        return False

    return True


def predict_probabilities(data_from_user):
    probabilities = loaded_model.predict_proba(data_from_user)
    return probabilities
