<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Emailer</title>
	<meta name="description" lang="en" content="">
	<meta name="keywords" lang="en" content="">
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
</head>

<body style="margin: 0;">
	
	<table style="max-width: 600px; margin: 0 auto; text-align: center; font-family: Helvetica, 'sans-serif'; color: #808080; line-height: 30px;">
		
		<thead style="background-color: #f7f7f7;">
			<tr>
				<td style="padding: 50px;">
					<img src="logo.png" alt="Logo" style="width: 100%; height: auto;">
				</td>
			</tr>
		</thead>
		
		<tbody>
			<tr>
				<td>
					<h2 style="font-size: 40px; color: #000000">Happy to help!</h2>
				</td>
			</tr>
			<tr>
				<td>
					<table>
						<tr>
							<td>
								<p>{% set hour = frappe.utils.now_datetime().hour %} {% if hour < 12 %} Good Morning{% if doc.contact %} {{ doc.contact }}{% endif %}!</p>
							</td>
						</tr>
						<tr>
							<td>
								<p>{% elif 12 < hour < 17 %} Good Afternoon{% if doc.contact %} {{ doc.contact }}{% endif %}!</p>
							</td>
						</tr>
						<tr>
							<td>
								<p>{% else %} Good Evening{% if doc.contact %} {{ doc.contact }}{% endif %}!</p>
							</td>
						</tr>
						<tr>
							<td>
								<p>{% endif %} This is an auto-generated email based on your recent support ticket. Here’s a summary.</p>
							</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr style="background-color: #f7f7f7;">
				<td>
					<table style="width: 100%; padding: 20px;">
						<tr>
							<td>
								<p style ="margin: 3px 0;"><b>Ticket ID: </b><a href="#" style="color: #00ADD8">{{ doc.name }}</a></p>
							</td>
						</tr>
						<tr>
							<td>
								<p style ="margin: 3px 0;"><b>This is regarding: </b>{{ doc.subject }}</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style ="margin: 3px 0;"><b>Description: </b>{{ doc.description | truncate(255, False, "...") }}</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style ="margin: 60px 0 10px;"><b>Expected response by:</b> {{ frappe.utils.add_to_date(frappe.utils.now_datetime(), hours=24).strftime('%A, %B %d, %I:%M %p') }}</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style ="margin: 3px 0;"><b>Assigned to:</b>
								{% set assign_users = frappe.db.get_all("Issue", filters={"name": doc.name}, fields=["_assign"])%}
								{% for assign_user in assign_users %}
									{% for key, value in assign_user.items() %}
										{{value|json(', ') }}
									{% endfor %}
								{% endfor %}
								</p>
							</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td>
					<table>
						<tr>
							<td>
								<p>Thanks for reaching out to us about your issue. Reply to this email if there’s anything else you’d want to add to this.</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style="margin: 0;">:)</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style="margin: 0;">Warmest Regards</p>
							</td>
						</tr>
						<tr>
							<td>
							{% set assign_users = frappe.db.get_all("Issue", filters={"name": doc.name}, fields=["_assign"])%}
								{% for assign_user in assign_users %}
									{% for key, value in assign_user.items() %}
										<p style="margin: 0;">{{value|json(', ') }}</p>
									{% endfor %}
								{% endfor %}
							</td>
						</tr>
					</table>
				</td>
			</tr>
		</tbody>
		
		<tfoot style="background-color: #14171a;">
			<tr>
				<td style="padding: 60px;">
					<table style="width: 100%;">
						<tr>
							<td>
								<p style="color: #fff; margin: 0;">Copyright &copy;2020 Bloomstack Inc, All rights reserved.</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style="color: #fff; margin: 30px 0 0;">Our support address is:</p>
							</td>
						</tr>
						<tr>
							<td>
								<p style="margin: 0;"><a href="emailto:support@bloomstack.com" style="color: #00ADD8">support@bloomstack.com</a></p>
							</td>
						</tr>
					</table>
				</td>
			</tr>
		</tfoot>
		
	</table>
	
</body>
</html>