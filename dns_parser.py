#!/usr/bin/python


# parse AD DNS logs


# regex examples ###############
#grab the names uncorrected, eg '(3)foo(6)domain(3)org(0)'
#       \([0-9]*\)[a-z0-9]* 
#remove the dumb 'empty' lines from windows DNS log, which include (?)trailing(?) whitespaces.
#       sed '/^[[:space:]]*$/d;s/[[:space:]]*$//' short_DNS_example
#an ipv4 address
#       [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+


import socket
import argparse
import re
import sys
import json
from dateutil import parser
from datetime import datetime,timedelta
import string


def reverse_lookup(address):
	try:
                return socket.gethostbyaddr(address)[0]
        except:
                return address

def strip_elements(line):
	try:
		date=find_mm_dd_yyyy_from_line(line)
		source_ip=first_ip_from_line(line)
		fqdn=find_domain_name(line)
	except Exception as err:
		raise ValueError('could not strip elements')
	return date,source_ip,fqdn



def first_ip_from_line(line):
	ip=re.compile('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
        ip_match=ip.findall(line)
	if ip_match:
		return ip_match[0]
	else:
		return 0


def find_mm_dd_yyyy_from_line(line):
	my_date=re.compile('[0-9]+\/[0-9]+\/[0-9][0-9][0-9][0-9]')
	my_date_match=my_date.findall(line)
	return my_date_match[0]

def find_domain_name(line):
	name_dirty=re.search("\([0-9]*\)[a-z0-9\-()]+", line)
	if name_dirty:
		name_clean=re.sub(r'\([0-9]+\)', ".", name_dirty.group(0))[1:-1]
		if 'in-addr.arpa' in name_clean:
			new_name=name_clean.split('.')
			name_clean=str('.'.join(new_name[3::-1]))
		return name_clean
	else:
		return 0


class dns_results():
	query=[]
	response=[]
	reverse_lookups={}

	def __init__(self):
		self.query=[]
		self.response=[]
		self.reverse_lookups={}
	#NEEDS WORK: splitting the logic from main into a class function 
	def print_results():
		print 'Direction        Date            Host                    Response'	



	#NEEDS WORK: splitting the logic from main into a class function
	def load_dns_log(self,file_f,load_date,lookup_reverse,site_name,query,response):
		for line in open(file_f):
                        #if date flag is used, skip lines not matching the date flag.
                        if load_date:
                                if load_date not in line:
                                        continue
                        try:
                                date,source_ip,fqdn=strip_elements(line)
                                if lookup_reverse and 'in-addr(4)arpa' in line:
                                        try:
                                                if fqdn not in self.reverse_lookups:
                                                        self.reverse_lookups[fqdn]=reverse_lookup(fqdn)
                                                        fqdn=reverse_lookups(fqdn)
                                                else:
                                                        fqdn=reverse_lookups[fqdn]+' (reverse lookup)'
                                        except:
                                                fqdn=fqdn+' (reverse lookup failed)'
                                elif 'in-addr.arpa' in line:
                                        fqdn=fqdn+' (reverse lookup)'

                                if site_name:
                                        if site_name not in fqdn:
                                                continue

                                if not isinstance(date,str) or not isinstance(source_ip,str) or not isinstance(fqdn,str):
                                        #print error message about line?
                                        continue

                                if ' R Q [' in line and 'UDP Snd' in line:
                                        if response:
                                                self.response.append(date+"    "+source_ip+"   "+fqdn)
                                                #print 'Response:        '+date+"        "+source_ip+"           "+fqdn
						
                                elif ' Q ['  in line and 'UDP Rcv'  in line:
                                        if query:
                                                self.query.append(date+"    "+source_ip+"   "+fqdn) 
                                                #print 'Query:           '+date+"        "+source_ip+"           "+fqdn

                        except ValueError:
                                continue

                        except TypeError:
                                continue

                        except KeyboardInterrupt:
                                break



def main():
	parser = argparse.ArgumentParser(description="Windows DNS parsing stuff.")
	parser.add_argument('-f', '--file', help='File to inspect')
	parser.add_argument('-Q', action='store_true', help='Print Queries')
	parser.add_argument('-R', action='store_true', help='Print Responses')
	parser.add_argument('-V', action='store_true', help='Perform reverse lookups')
	parser.add_argument('-d', help='Target date, mm/dd/yyyy format.')
	parser.add_argument('-s', help='target domain name')
	args=parser.parse_args()


	try:
		query=[]
                response=[]
		reverse_lookups={}

		# Check that the date has correct format.
		if args.d:
			if not re.search('[0-9]+\/[0-9]+\/[0-9][0-9][0-9][0-9]',args.d):	
				raise LookupError			

		print 'Direction	Date		Host			Response'
		for line in open(args.file):

			#if date flag is used, skip lines not matching the date flag.
			if args.d:
				if args.d not in line:
					continue
			try:
				date,source_ip,fqdn=strip_elements(line)
				if args.V and 'in-addr(4)arpa' in line:
					try:
						if fqdn not in reverse_lookups:
							reverse_lookups[fqdn]=reverse_lookup(fqdn)
							fqdn=reverse_lookups(fqdn)
						else:
							fqdn=reverse_lookups[fqdn]+' (reverse lookup)'
					except:
						fqdn=fqdn+' (reverse lookup failed)'
				elif 'in-addr.arpa' in line:
					fqdn=fqdn+' (reverse lookup)'

				if args.s:
					if args.s not in fqdn:
						continue

				if not isinstance(date,str) or not isinstance(source_ip,str) or not isinstance(fqdn,str):
					#print error message about line?
					continue

				if ' R Q [' in line and 'UDP Snd' in line:
					if args.R:
						#response.append(date+"    "+source_ip+"   "+fqdn)
						print 'Response:	'+date+"	"+source_ip+"		"+fqdn
				elif ' Q ['  in line and 'UDP Rcv'  in line:
					if args.Q:
						#query.append(date+"    "+source_ip+"   "+fqdn)	
						print 'Query:		'+date+"	"+source_ip+"		"+fqdn

			except ValueError:
				continue	

			except TypeError:
				continue
			
			except KeyboardInterrupt:
				break 	

			#if success, append.... 			
			#if type(date) is str and type(source_ip) is str and type(fqdn) is str:
			#	print 'yay'
			#else:
		#		continue
			#print date+"|"+source_ip+"|"+fqdn


#		if not ( args.R and args.Q ):
#			if args.R:
#				for entry in response:
#					print entry
#			if args.Q:
#				for entry in query:
#					print entry
#		else:
#			raise SyntaxError("Command flags -R and -Q are mutually exclusive")

	except LookupError:
		print 'invalid date format'
	except Exception:
		print 'Usage: jdns [-RQ] [-d date] [-s FQDN] -f dns_log'


	test=dns_results()
	test.load_dns_log(args.file,args.d,args.V,args.s,args.Q,args.R)
	print test.response


if __name__ == "__main__":
        main()
