from flask import Flask, render_template, request, send_file,make_response, redirect
import re, datetime, pathlib, os, requests
from werkzeug.utils import secure_filename
success = '<div class="alert alert-success" role="alert" style="text-align: center;"><h4>Выполнено</h4></div>'
no_ext = '<div class="alert alert-danger" role="alert" style="text-align: center;"><h4>Номеров нет</h4></div>'
val_error  = '<div class="alert alert-danger" role="alert" style="text-align: center;"><h4>Ошибка</h4></div>'
no_missed_values = '<div class="alert alert-success" role="alert" style="text-align: center;"><h4>В указанном диапазоне нет пропущенных значений</h4></div>'
no_file = '<div class="alert alert-danger" role="alert" style="text-align: center;"><h4>Файл не выбран</h4></div>'
ext_error = '<div class="alert alert-danger" role="alert" style="text-align: center;"><h4>Недостаточно МАС</h4></div>'
phone_error  = '<div class="alert alert-danger" role="alert" style="text-align: center;"><h4>Неверный номер телефона</h4></div>'
phone_link = '<a class="btn btn-success" href="https://www.spravportal.ru/Services/PhoneCodes/MobilePhoneInfo.aspx" role="button" target="_blank">Проверка переноса номера</a>'
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = 'tmp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def logging(str):
	with open ('logging.txt','a') as l:
		l.write(str + '\n')


@app.route('/index',methods=['POST','GET'])
def index() -> str:
	return render_template('index.html')

@app.route('/notes',methods=['POST','GET'])
def notes() -> str:
	return render_template('notes.html')
	
@app.route('/sql_query',methods=['POST','GET'])
def sql_query() -> str:
	return render_template('sql_query.html')

@app.route('/instructions',methods=['POST','GET'])
def instructions() -> str:
	return render_template('instructions.html')

@app.route('/sql_calls_query',methods=['POST','GET'])
def sql_calls_query() -> str:
	logging(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ': ' + 'выборка всех звонков')
	return ('', 204)
	
@app.route('/services', methods=['POST','GET'])
def services() -> 'html':
	try:
		extensions = request.form['data']
	except Exception as err:
		return render_template('services.html')
	resmult = []
	comp = re.compile(r'\s[7-8]\d{4}\s')
	extension_result = re.findall(comp, extensions)
	if extension_result:
		extension_result = [line.strip() for line in extension_result]
	else:
		 return render_template('services.html', ext = no_ext)
	extension_min = int(min(extension_result))
	for p in range(int(max(extension_result)) - int(min(extension_result))):
		if str(extension_min) not in extension_result:
			resmult.append(str(extension_min))
		extension_min += 1
	final_result = ';'.join(resmult)
	if not resmult: resmult.append('Свободных номеров нет')
	logging(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ': ' + 'поиск extension')
	ext_free = 'Свободные extension: ' + str(len(resmult))
	return render_template('services.html', ext = ext_free,output = resmult)

@app.route('/services_addext', methods=['POST','GET'])
def services_addext() -> 'html':
	try:
		strrem = request.form['data_ext']
		mac = request.form['data_mac']
	except Exception as err:
		return render_template('services_addext.html')
	extension_list = []
	strrem = strrem.replace(' ', '')
	strrem = strrem.rstrip(';')
	extension_list = strrem.split(';')
	mac = mac.replace('\n','')
	mac_list = mac.split('\r')
	if len(extension_list) < len(mac_list):
		return render_template('services_addext.html', suc = ext_error)
	else:
		try:
			res_file = open('1res_file.txt', 'w')			
			res_file.write('MAC ADDRESS,DESCRIPTION,DIRECTORY NUMBER 1' + '\n')
			for res in mac_list:
				res_file.write('SEP' + res + ',' + res + ',' + extension_list.pop() + '\n')
			res_file.close()    
			logging(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ': ' + 'массовая привязка MAC')  
		except Exception as err:
			print('Что-то пошло не так ', str(err))
	

	return render_template('services_addext.html', suc = success, link = '<a href="/download">Скачать файл</a>')


@app.route('/download', methods=['POST','GET'])
def download():
	p = '1res_file.txt'
	resp = make_response(send_file(p, as_attachment=True))
	resp.cache_control.max_age = 'no-store'
	return(resp)

@app.route('/download_mac', methods=['POST','GET'])
def download_mac():
	p = 'result.txt'
	resp = make_response(send_file(p, as_attachment=True))
	resp.cache_control.max_age = 'no-store'
	return(resp)

@app.route('/services_missval', methods=['POST','GET'])
def services_missval() -> 'html':
	try:
		val = request.form['data_missval']
	except Exception as err:
		return render_template('services_missval.html')
	message = ''
	result = []
	exist_finesse = []
	try:
		val = val.replace('\n', '')
		exist_finesse = val.split('\r')
		min_val = int(min(exist_finesse))
		diff = int(max(exist_finesse)) - int(min(exist_finesse)) + 1
		
		final_result = []
		for p in range(diff):
			if str(min_val) not in exist_finesse:
				result.append(str(min_val))
			min_val += 1
		message = 'Список найденных значений: ' + str(len(result))
		if len(result) == 0:
			message = no_missed_values
		logging(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ': ' + 'поиск пропущенных значений')
	except Exception as err:
		print('Что-то пошло не так ', str(err))
		message = val_error	
	
	return render_template('services_missval.html', values_list = result,val = message)


@app.route('/services_macclear', methods=['POST','GET'])
def services_macclear() -> 'html':
	try:
		file = request.files['choosen_file']
		old_ext = request.form['data_oldext']
		if len(file.filename) == 0:			
			return render_template('services_macclear.html', val = no_file)
	except Exception as err:
		return render_template('services_macclear.html')

	
	if file and allowed_file(file.filename):
		finalstr = []
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		ext_for_remove = old_ext.replace(' ', '')
		ext_for_remove = ext_for_remove.rstrip(';')
		ext_for_remove_list = ext_for_remove.split(';')
		backup_filename = 'BACKUP_FILE_' + str(datetime.datetime.now().strftime('%Y_%m_%d %H_%M_%S')) + '.txt'
		
		backup_file = open(os.getcwd() + '/tmp/' + backup_filename, 'w')		
		backup_file.write('MAC ADDRESS,DESCRIPTION,DIRECTORY NUMBER 1' + '\n')
		
		for item in ext_for_remove_list:
			with open('tmp/' + file.filename) as f:
				for line in f:
					if (line.find(item.strip()) != -1 and line.find('Registered') == -1 and line.find('Unregistered') == -1):
						finalstr.append(line)
						comp_backup = re.compile(r'SEP[0-9A-F]{12}')
						st_backup = re.findall(comp_backup, line)
						mac_backup = ''
						try:
							mac_backup = st_backup[0][3:15]
							backup_file.write('SEP' + mac_backup + ',' + mac_backup + ',' + item + '\n')
						except Exception as err:
							pass
		backup_file.close()
							
					
		st = ''
		with open ('result.txt','w') as r:
			r.write('DESCRIPTION' + '\n')
			comp = re.compile(r'SEP[0-9A-F]{12}')
			for z in finalstr:
				st = re.findall(comp, z)
				try:
					string = st[0][3:15]
					r.write(string + '\n')
				except Exception as err:
					pass
		logging(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ': ' + 'чистка MAC')		
		return render_template('services_macclear.html', val = success, link = '<a href="/download_mac">Скачать файл</a>')
	else:
		return render_template('services_macclear.html', val = val_error)

@app.route('/services_phonecheck', methods=['POST','GET'])
def services_phonecheck() -> 'html':
	url_phone = 'http://phoneverify.org/api.pl?&id=phoneinfo&email=evgeniygrebenkin@gmail.com&password=0b87f3566d15ccc96d7c62eb32a1402f&phone=' 
	response_dict = {}
	try:
		phone = request.form['phone_number']
		url_phone = url_phone + phone + '&format=json'
		r = requests.get(url_phone)
		response_dict = r.json()
		if response_dict['status'] == '203':
			return render_template('services_phonecheck.html', err = phone_error, out_dict = response_dict)
		logging(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ': ' + 'проверка номера телефона')
		return render_template('services_phonecheck.html', phone_num = 'Телефон: ', operator = 'Оператор: ', region = 'Регион: ', city = 'Город: ', prefix = 'Префикс: ', last_upd = 'Последнее обновление: ', phone_number = phone, link = phone_link, out_dict = response_dict)
	except:
		return render_template('services_phonecheck.html', out_dict = response_dict)

app.run(host='0.0.0.0', debug=True)