from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    edas_id = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    remark = models.CharField(max_length=200, blank=True, null=True)
    page_no = models.IntegerField(blank=True, null=True)
    authors = models.ManyToManyField(User)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_us = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    def get_authors_text(self):
        text = ''
        for author in self.authors.all():
            text += author.get_full_name()
        return text

    def get_status(self):
        if self.is_paid:
            return "Paid"
        else:
            return "Not paid"


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    COUNTRIES = (
        ('AF', 'Afghanistan',),
        ('AX', 'Aland Islands',),
        ('AL', 'Albania',),
        ('DZ', 'Algeria',),
        ('AS', 'American Samoa',),
        ('AD', 'Andorra',),
        ('AO', 'Angola',),
        ('AI', 'Anguilla',),
        ('AQ', 'Antarctica',),
        ('AG', 'Antigua and Barbuda',),
        ('AR', 'Argentina',),
        ('AM', 'Armenia',),
        ('AW', 'Aruba',),
        ('AU', 'Australia',),
        ('AT', 'Austria',),
        ('AZ', 'Azerbaijan',),
        ('BS', 'Bahamas',),
        ('BH', 'Bahrain',),
        ('BD', 'Bangladesh',),
        ('BB', 'Barbados',),
        ('BY', 'Belarus',),
        ('BE', 'Belgium',),
        ('BZ', 'Belize',),
        ('BJ', 'Benin',),
        ('BM', 'Bermuda',),
        ('BT', 'Bhutan',),
        ('BO', 'Bolivia, Plurinational State of',),
        ('BQ', 'Bonaire, Sint Eustatius and Saba',),
        ('BA', 'Bosnia and Herzegovina',),
        ('BW', 'Botswana',),
        ('BV', 'Bouvet Island',),
        ('BR', 'Brazil',),
        ('IO', 'British Indian Ocean Territory',),
        ('BN', 'Brunei Darussalam',),
        ('BG', 'Bulgaria',),
        ('BF', 'Burkina Faso',),
        ('BI', 'Burundi',),
        ('KH', 'Cambodia',),
        ('CM', 'Cameroon',),
        ('CA', 'Canada',),
        ('CV', 'Cape Verde',),
        ('KY', 'Cayman Islands',),
        ('CF', 'Central African Republic',),
        ('TD', 'Chad',),
        ('CL', 'Chile',),
        ('CN', 'China',),
        ('CX', 'Christmas Island',),
        ('CC', 'Cocos (Keeling) Islands',),
        ('CO', 'Colombia',),
        ('KM', 'Comoros',),
        ('CG', 'Congo',),
        ('CD', 'Congo, the Democratic Republic of the',),
        ('CK', 'Cook Islands',),
        ('CR', 'Costa Rica',),
        ('CI', "Cote d'Ivoire",),
        ('HR', 'Croatia',),
        ('CU', 'Cuba',),
        ('CW', 'Curacao',),
        ('CY', 'Cyprus',),
        ('CZ', 'Czech Republic',),
        ('DK', 'Denmark',),
        ('DJ', 'Djibouti',),
        ('DM', 'Dominica',),
        ('DO', 'Dominican Republic',),
        ('EC', 'Ecuador',),
        ('EG', 'Egypt',),
        ('SV', 'El Salvador',),
        ('GQ', 'Equatorial Guinea',),
        ('ER', 'Eritrea',),
        ('EE', 'Estonia',),
        ('ET', 'Ethiopia',),
        ('FK', 'Falkland Islands (Malvinas)',),
        ('FO', 'Faroe Islands',),
        ('FJ', 'Fiji',),
        ('FI', 'Finland',),
        ('FR', 'France',),
        ('GF', 'French Guiana',),
        ('PF', 'French Polynesia',),
        ('TF', 'French Southern Territories',),
        ('GA', 'Gabon',),
        ('GM', 'Gambia',),
        ('GE', 'Georgia',),
        ('DE', 'Germany',),
        ('GH', 'Ghana',),
        ('GI', 'Gibraltar',),
        ('GR', 'Greece',),
        ('GL', 'Greenland',),
        ('GD', 'Grenada',),
        ('GP', 'Guadeloupe',),
        ('GU', 'Guam',),
        ('GT', 'Guatemala',),
        ('GG', 'Guernsey',),
        ('GN', 'Guinea',),
        ('GW', 'Guinea-Bissau',),
        ('GY', 'Guyana',),
        ('HT', 'Haiti',),
        ('HM', 'Heard Island and McDonald Islands',),
        ('VA', 'Holy See (Vatican City State)',),
        ('HN', 'Honduras',),
        ('HK', 'Hong Kong',),
        ('HU', 'Hungary',),
        ('IS', 'Iceland',),
        ('IN', 'India',),
        ('ID', 'Indonesia',),
        ('IR', 'Iran, Islamic Republic of',),
        ('IQ', 'Iraq',),
        ('IE', 'Ireland',),
        ('IM', 'Isle of Man',),
        ('IL', 'Israel',),
        ('IT', 'Italy',),
        ('JM', 'Jamaica',),
        ('JP', 'Japan',),
        ('JE', 'Jersey',),
        ('JO', 'Jordan',),
        ('KZ', 'Kazakhstan',),
        ('KE', 'Kenya',),
        ('KI', 'Kiribati',),
        ('KP', "Korea, Democratic People's Republic of",),
        ('KR', 'Korea, Republic of',),
        ('KW', 'Kuwait',),
        ('KG', 'Kyrgyzstan',),
        ('LA', "Lao People's Democratic Republic",),
        ('LV', 'Latvia',),
        ('LB', 'Lebanon',),
        ('LS', 'Lesotho',),
        ('LR', 'Liberia',),
        ('LY', 'Libya',),
        ('LI', 'Liechtenstein',),
        ('LT', 'Lithuania',),
        ('LU', 'Luxembourg',),
        ('MO', 'Macao',),
        ('MK', 'Macedonia, the former Yugoslav Republic of',),
        ('MG', 'Madagascar',),
        ('MW', 'Malawi',),
        ('MY', 'Malaysia',),
        ('MV', 'Maldives',),
        ('ML', 'Mali',),
        ('MT', 'Malta',),
        ('MH', 'Marshall Islands',),
        ('MQ', 'Martinique',),
        ('MR', 'Mauritania',),
        ('MU', 'Mauritius',),
        ('YT', 'Mayotte',),
        ('MX', 'Mexico',),
        ('FM', 'Micronesia, Federated States of',),
        ('MD', 'Moldova, Republic of',),
        ('MC', 'Monaco',),
        ('MN', 'Mongolia',),
        ('ME', 'Montenegro',),
        ('MS', 'Montserrat',),
        ('MA', 'Morocco',),
        ('MZ', 'Mozambique',),
        ('MM', 'Myanmar',),
        ('NA', 'Namibia',),
        ('NR', 'Nauru',),
        ('NP', 'Nepal',),
        ('NL', 'Netherlands',),
        ('NC', 'New Caledonia',),
        ('NZ', 'New Zealand',),
        ('NI', 'Nicaragua',),
        ('NE', 'Niger',),
        ('NG', 'Nigeria',),
        ('NU', 'Niue',),
        ('NF', 'Norfolk Island',),
        ('MP', 'Northern Mariana Islands',),
        ('NO', 'Norway',),
        ('OM', 'Oman',),
        ('PK', 'Pakistan',),
        ('PW', 'Palau',),
        ('PS', 'Palestine, State of',),
        ('PA', 'Panama',),
        ('PG', 'Papua New Guinea',),
        ('PY', 'Paraguay',),
        ('PE', 'Peru',),
        ('PH', 'Philippines',),
        ('PN', 'Pitcairn',),
        ('PL', 'Poland',),
        ('PT', 'Portugal',),
        ('PR', 'Puerto Rico',),
        ('QA', 'Qatar',),
        ('RE', 'Reunion',),
        ('RO', 'Romania',),
        ('RU', 'Russian Federation',),
        ('RW', 'Rwanda',),
        ('BL', 'Saint Barthelemy',),
        ('SH', 'Saint Helena, Ascension and Tristan da Cunha',),
        ('KN', 'Saint Kitts and Nevis',),
        ('LC', 'Saint Lucia',),
        ('MF', 'Saint Martin (French part)',),
        ('PM', 'Saint Pierre and Miquelon',),
        ('VC', 'Saint Vincent and the Grenadines',),
        ('WS', 'Samoa',),
        ('SM', 'San Marino',),
        ('ST', 'Sao Tome and Principe',),
        ('SA', 'Saudi Arabia',),
        ('SN', 'Senegal',),
        ('RS', 'Serbia',),
        ('SC', 'Seychelles',),
        ('SL', 'Sierra Leone',),
        ('SG', 'Singapore',),
        ('SX', 'Sint Maarten (Dutch part)',),
        ('SK', 'Slovakia',),
        ('SI', 'Slovenia',),
        ('SB', 'Solomon Islands',),
        ('SO', 'Somalia',),
        ('ZA', 'South Africa',),
        ('GS', 'South Georgia and the South Sandwich Islands',),
        ('SS', 'South Sudan',),
        ('ES', 'Spain',),
        ('LK', 'Sri Lanka',),
        ('SD', 'Sudan',),
        ('SR', 'Suriname',),
        ('SJ', 'Svalbard and Jan Mayen',),
        ('SZ', 'Swaziland',),
        ('SE', 'Sweden',),
        ('CH', 'Switzerland',),
        ('SY', 'Syrian Arab Republic',),
        ('TW', 'Taiwan, Province of China',),
        ('TJ', 'Tajikistan',),
        ('TZ', 'Tanzania, United Republic of',),
        ('TH', 'Thailand',),
        ('TL', 'Timor-Leste',),
        ('TG', 'Togo',),
        ('TK', 'Tokelau',),
        ('TO', 'Tonga',),
        ('TT', 'Trinidad and Tobago',),
        ('TN', 'Tunisia',),
        ('TR', 'Turkey',),
        ('TM', 'Turkmenistan',),
        ('TC', 'Turks and Caicos Islands',),
        ('TV', 'Tuvalu',),
        ('UG', 'Uganda',),
        ('UA', 'Ukraine',),
        ('AE', 'United Arab Emirates',),
        ('GB', 'United Kingdom',),
        ('US', 'United States',),
        ('UM', 'United States Minor Outlying Islands',),
        ('UY', 'Uruguay',),
        ('UZ', 'Uzbekistan',),
        ('VU', 'Vanuatu',),
        ('VE', 'Venezuela, Bolivarian Republic of',),
        ('VN', 'Viet Nam',),
        ('VG', 'Virgin Islands, British',),
        ('VI', 'Virgin Islands, U.S.',),
        ('WF', 'Wallis and Futuna',),
        ('EH', 'Western Sahara',),
        ('YE', 'Yemen',),
        ('ZM', 'Zambia',),
        ('ZW', 'Zimbabwe',),
    )
    country = models.CharField(max_length=2, choices=COUNTRIES)
    ieee = models.CharField(max_length=20, blank=True, null=True)
    is_ugm = models.BooleanField(default=False)


class AdditionalItem(models.Model):
    name = models.CharField(max_length=50)
    remark = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_us = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Payment(models.Model):
    code = models.CharField(max_length=20)
    remark = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    METHODS = (
        ('C', 'Credit Card'),
        ('T', 'Bank Transfer'),
    )
    method = models.CharField(max_length=1, choices=METHODS)
    slip = models.ImageField(upload_to='slips/', null=True, blank=True)
    confirm = models.BooleanField(default=False)
    del_flag = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_create_by')
    delete_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_delete_by')

    def get_method_text(self):
        return [t for t in self.METHODS if t[0] == self.method]


class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    add_item = models.ForeignKey(AdditionalItem, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    CURRENCIES = (
        ('THB', 'Thai Baht'),
        ('USD', 'US Dollar'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCIES)
