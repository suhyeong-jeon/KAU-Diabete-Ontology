from flask import Flask, render_template, request, redirect, url_for
from owlready2 import *


app = Flask(__name__)

host_addr = "0.0.0.0"
port_num = "8000"

global reasoning_result
reasoning_result = {}
global reasoning_result2
reasoning_result2 = []
global count
count = 0


@app.route('/', methods=('GET','POST')) # 접속하는 url
def signup_page():
    global count
    global reasoning_result
    global reasoning_result2
    reasoning_result = {}
    reasoning_result2 = []

    # onto = get_ontology("/Users/jeonsuhyeong/Desktop/Untitled.owl").load()
    if request.method == "POST":
        print(f'hasHypoglycemia : {request.form.get("hasHypoglycemia")}\n'
              f'patient_heart_condition : {request.form.get("patient_heart_condition")}\n'
              f'patient_liver_condition : {request.form.get("patient_liver_condition")}\n'
              f'patient_kidney_condition : {request.form.get("patient_kidney_condition")}\n'
              f'patient_stomach_condition : {request.form.get("patient_stomach_condition")}\n'
              f'patient_pancreas_condition : {request.form.get("patient_pancreas_condition")}\n'
              f'patient_age : {request.form.get("patient_age")}\n'
              f'patient_fastingBG : {request.form.get("patient_fastingBG")}\n'
              f'patient_cpep : {request.form.get("patient_cpep")}\n'
              f'patient_insulin : {request.form.get("patient_insulin")}\n'
              f'patient_bloodpressure : {request.form.get("patient_bloodpressure")}\n') # 안전하게 가져오려면 get
        user = request.form.get('Post')
        data = {'level': 60, 'point': 360, 'exp': 45000}


        onto = get_ontology("../final.owl").load()

        class 정상간(Thing):
            namespace = onto
        class 간장애(Thing):
            namespace = onto
        class 가족력(Thing):
            namespace = onto
        class 갑상선암(Thing):
            namespace = onto
        class 정상신장(Thing):
            namespace = onto
        class 신장질환(Thing):
            namespace = onto
        class 정상심장(Thing):
            namespace = onto
        class 심장질환(Thing):
            namespace = onto
        class 정상위(Thing):
            namespace = onto
        class 위질환(Thing):
            namespace = onto
        class 정상췌장(Thing):
            namespace = onto
        class 췌장장애(Thing):
            namespace = onto
        class 다발성_내분비성_중증(Thing):
            namespace = onto

        class has(ObjectProperty):
            namespace = onto

        with onto:
            class hasCpep(DataProperty, FunctionalProperty):
                # domain = [정상간]
                range = [float]
            class hasHypoglycemia(DataProperty, FunctionalProperty):
                # domain = [정상간]
                range = [float]
            class hasAgeof(DataProperty, FunctionalProperty):
                # domain = [정상간]
                range = [float]
            class hasFastingBG(DataProperty, FunctionalProperty):
                # domain = [정상간]
                range = [float]
            class hasValue(DataProperty, FunctionalProperty):
                range = [float]
            class hasTwoHourBG(DataProperty, FunctionalProperty):
                range = [float]
            class hasrandomBG(DataProperty, FunctionalProperty):
                range = [float]
            class has경구포도당(DataProperty, FunctionalProperty):
                range = [float]
        count += 1
        patient_name = f'user_patient_{count}'
        print('patient_name: ' , patient_name)

        if (request.form.get("patient_heart_condition") == 1):
            patient_name = 심장질환('user_patient')
        else:
            patient_name = 정상심장('user_patient')

        if (request.form.get("patient_liver_condition") == 1) :
            patient_name = 간장애('user_patient')
        else:
            patient_name = 정상간('user_patient')

        if (request.form.get("patient_kidney_condition") == 1) :
            patient_name = 신장질환('user_patient')
        else:
            patient_name = 정상신장('user_patient')

        if (request.form.get("patient_stomach_condition") == 1) :
            patient_name = 위질환('user_patient')
        else:
            patient_name = 정상위('user_patient')

        if (request.form.get("patient_pancreas_condition") == 1) :
            patient_name = 췌장장애('user_patient')
        else:
            patient_name = 정상췌장('user_patient')

        if (request.form.get("hascancer") == 0) :
            patient_name.is_a.append(Not(has.some((갑상선암))))

        if (request.form.get("hasdiversedisease") == 1) :
            patient_name.is_a.append(Not(has.some((다발성_내분비성_중증))))

        if (request.form.get("hasfamilyhistory") == 1) :
            patient_name.is_a.append(Not(has.some((가족력))))


        patient_name.hasCpep = float(request.form.get("patient_cpep"))
        patient_name.hasHypoglycemia = float(request.form.get("hasHypoglycemia"))
        patient_name.hasAgeof = float(request.form.get("patient_age"))
        patient_name.hasFastingBG = float(request.form.get("patient_fastingBG"))
        patient_name.hasValue = float(request.form.get("patient_bmi"))
        patient_name.hasTwoHourBG = float(request.form.get("patient_2hourBG"))
        patient_name.has경구포도당 = float(request.form.get("patient_pododang"))


        individuals_list = list(onto.individuals()) # individuals 리스트\
        print(individuals_list)
        print(patient_name.get_properties())
        print(patient_name.is_a)
        try:
            sync_reasoner()

            query_instance = str(patient_name).replace('final.', '')
            print(
            list(default_world.sparql(f"""
            SELECT ?property ?value
            WHERE {{
              final:{query_instance} ?property ?value .
            }}
            """))
            )

            # sparql_query = list(default_world.sparql(f"""
            # SELECT ?subject ?predicate ?object
            # WHERE {{
            #   ?subject ?predicate ?object .
            #   ?subject rdf:type final:Sayagliptin .
            # }}
            #
            # """))
            # for result in sparql_query:
            #     print(result)


            for idx, inferred_class in enumerate(patient_name.is_a):
                reasoning_result[inferred_class] = idx

                changed_class = str(inferred_class).replace('final.', '')
                reasoning_result2.append(changed_class)
                print("추론된 클래스:", inferred_class)
        except Exception as e:
            print(f"에러 발생: {e}")
            reasoning_result2.append('투여가능한 약이 존재하지 않습니다.')



        return redirect(url_for('result'))  # /result로 리다이렉트
    else:
        return render_template('MainPage.html')  # GET 요청이면 홈 페이지를 렌더링

@app.route('/result', methods=('GET', 'POST'))
def result():
    abc = sorted(reasoning_result2)
    data = abc
    print("AA")
    # 여기에서 데이터를 처리하거나 원하는 작업을 수행할 수 있습니다.
    return render_template('Result.html', data = data)


if __name__ == "__main__":
    app.run(host=host_addr, port=port_num)
